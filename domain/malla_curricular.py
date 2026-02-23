from typing import List
from domain.materia import Materia

class MallaCurricular:
    def __init__(self, carrera: str):
        self._carrera = carrera
        self._materias: List[Materia] = []

    def get_carrera(self) -> str:
        return self._carrera

    def get_materias(self) -> List[Materia]:
        return self._materias

    def agregar_materia(self, materia: Materia) -> None:
        # Validación: evitar duplicar materias
        for m in self._materias:
            if m.get_id() == materia.get_id():
                raise ValueError(f"La materia con ID {materia.get_id()} ya se encuentra registrada.")
        self._materias.append(materia)

    def get_materias_por_semestre(self, semestre: int) -> List[Materia]:
        return [m for m in self._materias if m.get_semestre() == semestre]
