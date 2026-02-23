from typing import List, Optional
from domain.materia import Materia
# Importación diferida para no generar ciclos si hubiese, aunque se maneja con la abstracción
from strategy.filtro_strategy import FiltroStrategy

class CalculadoraPromedio:
    def __init__(self):
        self._filtro: Optional[FiltroStrategy] = None

    def set_filtro(self, filtro: FiltroStrategy) -> None:
        self._filtro = filtro

    def calcular(self, materias: List[Materia]) -> float:
        materias_a_procesar = self._filtro.filtrar(materias) if self._filtro else materias
        if not materias_a_procesar:
            return 0.0
            
        suma_productos = sum(m.get_nota() * m.get_creditos() for m in materias_a_procesar)
        suma_creditos = sum(m.get_creditos() for m in materias_a_procesar)
        
        if suma_creditos == 0:
            return 0.0
            
        return suma_productos / suma_creditos

    def calcular_por_semestre(self, materias: List[Materia], semestre: int) -> float:
        materias_sem = [m for m in materias if m.get_semestre() == semestre]
        return self.calcular(materias_sem)
