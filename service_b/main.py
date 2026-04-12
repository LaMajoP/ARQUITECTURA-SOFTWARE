from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging

# Configuración de observabilidad: logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de OpenTelemetry + Jaeger
resource = Resource.create({"service.name": "servicio-b"})
tracer_provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(tracer_provider)

app = FastAPI(title="Servicio Proveedor (Service B) - Materias Extra")

Instrumentator().instrument(app).expose(app)
FastAPIInstrumentor.instrument_app(app)

@app.get("/materias-extra")
def obtener_materias_extra():
    logger.info("Recibida petición de materias extra (GET /materias-extra)")
    
    # Simulamos el retorno de información adicional en formato JSON
    return {
        "materias_sugeridas": [
            {"nombre": "Liderazgo y Emprendimiento", "creditos": 2},
            {"nombre": "Innovación Tecnológica", "creditos": 3},
            {"nombre": "Ética Profesional", "creditos": 2},
            {"nombre": "Gestión de Proyectos", "creditos": 3}
        ]
    }
