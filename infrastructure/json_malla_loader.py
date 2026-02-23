import json
import os
from infrastructure.i_malla_loader import IMallaLoader
from domain.malla_curricular import MallaCurricular
from domain.materia import Materia

class JSONMallaLoader(IMallaLoader):
    def load(self, path: str) -> MallaCurricular:
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
            
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        malla = MallaCurricular(data.get("carrera", "Desconocida"))
        for mat_data in data.get("materias", []):
            materia = Materia(
                id=mat_data["id"],
                nombre=mat_data["nombre"],
                creditos=mat_data["creditos"],
                semestre=mat_data["semestre"],
                es_oficial=mat_data.get("esOficial", True)
            )
            malla.agregar_materia(materia)
            
        return malla
