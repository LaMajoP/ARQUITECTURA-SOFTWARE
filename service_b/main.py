from fastapi import FastAPI
import logging

# Configuración de observabilidad: logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Servicio Proveedor (Service B) - Materias Extra")

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
