from abc import ABC, abstractmethod
from typing import List
from domain.materia import Materia

class FiltroStrategy(ABC):
    @abstractmethod
    def filtrar(self, materias: List[Materia]) -> List[Materia]:
        pass

class FiltroIngles(FiltroStrategy):
    def filtrar(self, materias: List[Materia]) -> List[Materia]:
        return [m for m in materias if "inglés" not in m.get_nombre().lower()]

class FiltroElectivas(FiltroStrategy):
    def filtrar(self, materias: List[Materia]) -> List[Materia]:
        return [m for m in materias if "electiva" not in m.get_nombre().lower()]
