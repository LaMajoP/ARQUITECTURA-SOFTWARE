from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import requests
import time

from domain.materia import Materia
from domain.calculadora_promedio import CalculadoraPromedio

# Configuración de observabilidad: logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Servicio Principal de Calculadora de Promedios")

class MateriaInput(BaseModel):
    id: int
    nombre: str
    creditos: int
    semestre: int
    nota: float = 0.0
    es_oficial: bool = True

class PromedioRequest(BaseModel):
    materias: List[MateriaInput]

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

@app.post("/promedio")
def calcular_promedio(request: PromedioRequest):
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
