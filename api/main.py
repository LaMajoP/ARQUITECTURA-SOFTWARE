from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import logging
import requests
import time

from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from domain.materia import Materia
from domain.calculadora_promedio import CalculadoraPromedio
from api.auth import authenticate_user, create_access_token, get_current_user, require_role

# Configuración de observabilidad: logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de OpenTelemetry + Jaeger
resource = Resource.create({"service.name": "servicio-principal"})
tracer_provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(tracer_provider)

RequestsInstrumentor().instrument()

app = FastAPI(title="Servicio Principal de Calculadora de Promedios")

Instrumentator().instrument(app).expose(app)
FastAPIInstrumentor.instrument_app(app)

class LoginRequest(BaseModel):
    username: str
    password: str

class MateriaInput(BaseModel):
    id: int
    nombre: str
    creditos: int
    semestre: int
    nota: float = 0.0
    es_oficial: bool = True

class PromedioRequest(BaseModel):
    materias: List[MateriaInput]

class PromedioObjetivoRequest(BaseModel):
    materias_cursadas: List[MateriaInput]
    materias_pendientes: List[MateriaInput]
    promedio_objetivo: float

SERVICE_B_URL = "http://127.0.0.1:8001/materias-extra"

def obtener_materias_extra_con_reintento() -> List[dict]:
    """
    Llama a service_b para obtener materias extra.
    Implementa patrones de resiliencia: Timeout, Retry y Fallback.
    """
    logger.info("Llamando al servicio externo de materias extra...")
    max_retries = 3
    timeout_sec = 2.0
    
    for intento in range(max_retries):
        try:
            # 1. Timeout Pattern
            response = requests.get(SERVICE_B_URL, timeout=timeout_sec)
            response.raise_for_status()
            logger.info("Respuesta obtenida del servicio de materias extra exitosamente.")
            return response.json().get("materias_sugeridas", [])
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout al conectar con el servicio externo. Intento {intento + 1}/{max_retries}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error al conectar con el servicio externo: {e}. Intento {intento + 1}/{max_retries}")
        
        # 2. Retry Pattern (wait before next attempt)
        time.sleep(1)
    
    # 3. Fallback Pattern
    logger.error("No se pudo obtener respuesta del servicio externo tras varios intentos. Usando fallback (lista vacía).")
    return []

@app.post("/login")
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        logger.warning(f"Intento de login fallido para el usuario: {request.username}")
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos.")
    token = create_access_token(username=user["username"], role=user["role"])
    logger.info(f"Login exitoso para el usuario: {user['username']} con rol: {user['role']}")
    return {"access_token": token, "token_type": "bearer"}


@app.post("/promedio")
def calcular_promedio(request: PromedioRequest, current_user: dict = Depends(get_current_user)):
    logger.info("Iniciando cálculo de promedio...")
    
    # Transformar input DTO a objetos de dominio de la aplicación existente
    materias_dominio = []
    for m_in in request.materias:
        try:
            materia = Materia(
                id=m_in.id, 
                nombre=m_in.nombre, 
                creditos=m_in.creditos, 
                semestre=m_in.semestre, 
                es_oficial=m_in.es_oficial
            )
            materia.set_nota(m_in.nota)
            materias_dominio.append(materia)
        except ValueError as e:
            logger.error(f"Error de validación en materia {m_in.nombre}: {e}")
            raise HTTPException(status_code=400, detail=str(e))
            
    # Comunicación entre servicios (Llama a Service B)
    materias_extra = obtener_materias_extra_con_reintento()
    
    # Utilizar la lógica existente para calcular
    calculadora = CalculadoraPromedio()
    promedio = calculadora.calcular(materias_dominio)
    
    logger.info(f"Cálculo completado. Promedio ponderado: {promedio:.2f}")

    return {
        "promedio_calculado": round(promedio, 2),
        "materias_extra_sugeridas": materias_extra
    }

@app.post("/promedio-objetivo")
def calcular_nota_requerida(request: PromedioObjetivoRequest, current_user: dict = Depends(require_role("admin"))):
    logger.info("Calculando nota requerida para alcanzar promedio objetivo...")

    cursadas = []
    for m in request.materias_cursadas:
        try:
            materia = Materia(id=m.id, nombre=m.nombre, creditos=m.creditos,
                              semestre=m.semestre, es_oficial=m.es_oficial)
            materia.set_nota(m.nota)
            cursadas.append(materia)
        except ValueError as e:
            logger.error(f"Error de validación en materia cursada {m.nombre}: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    pendientes = []
    for m in request.materias_pendientes:
        try:
            materia = Materia(id=m.id, nombre=m.nombre, creditos=m.creditos,
                              semestre=m.semestre, es_oficial=m.es_oficial)
            materia.set_nota(0.0)
            pendientes.append(materia)
        except ValueError as e:
            logger.error(f"Error de validación en materia pendiente {m.nombre}: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    if not pendientes:
        raise HTTPException(status_code=400, detail="Debe enviar al menos una materia pendiente.")

    calculadora = CalculadoraPromedio()
    promedio_actual = calculadora.calcular(cursadas)

    creditos_cursados = sum(m.get_creditos() for m in cursadas)
    creditos_pendientes = sum(m.get_creditos() for m in pendientes)
    suma_ponderada_actual = sum(m.get_nota() * m.get_creditos() for m in cursadas)
    total_creditos = creditos_cursados + creditos_pendientes

    nota_requerida = (request.promedio_objetivo * total_creditos - suma_ponderada_actual) / creditos_pendientes
    es_alcanzable = nota_requerida <= 5.0

    materias_extra = obtener_materias_extra_con_reintento()

    logger.info(f"Nota requerida: {nota_requerida:.2f}. Alcanzable: {es_alcanzable}")

    return {
        "promedio_actual": round(promedio_actual, 2),
        "promedio_objetivo": request.promedio_objetivo,
        "creditos_cursados": creditos_cursados,
        "creditos_pendientes": creditos_pendientes,
        "nota_requerida_en_pendientes": round(nota_requerida, 2),
        "es_alcanzable": es_alcanzable,
        "materias_extra_sugeridas": materias_extra
    }
