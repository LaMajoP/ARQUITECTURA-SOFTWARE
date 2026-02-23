class Materia:
    def __init__(self, id: int, nombre: str, creditos: int, semestre: int, es_oficial: bool = True):
        self._id = id
        self._nombre = nombre
        self._creditos = creditos
        self._nota = 0.0
        self._cortes = {"corte1": 0.0, "corte2": 0.0, "corte3": 0.0}
        self._semestre = semestre
        self._es_oficial = es_oficial

    def get_id(self) -> int:
        return self._id

    def set_id(self, id: int) -> None:
        self._id = id

    def get_nombre(self) -> str:
        return self._nombre

    def set_nombre(self, nombre: str) -> None:
        self._nombre = nombre

    def get_creditos(self) -> int:
        return self._creditos

    def set_creditos(self, creditos: int) -> None:
        self._creditos = creditos

    def get_nota(self) -> float:
        return self._nota

    def set_nota(self, nota: float) -> None:
        if not (0.0 <= nota <= 5.0):
            raise ValueError("La nota debe estar entre 0.0 y 5.0")
        self._nota = nota

    def set_notas_cortes(self, corte1: float, corte2: float, corte3: float) -> None:
        if not all(0.0 <= c <= 5.0 for c in (corte1, corte2, corte3)):
            raise ValueError("Las notas de los cortes deben estar entre 0.0 y 5.0")
        self._cortes = {"corte1": corte1, "corte2": corte2, "corte3": corte3}
        nota_final = round((corte1 * 0.3) + (corte2 * 0.3) + (corte3 * 0.4), 1)
        self.set_nota(nota_final)

    def get_cortes(self) -> dict:
        return self._cortes

    def get_semestre(self) -> int:
        return self._semestre

    def set_semestre(self, semestre: int) -> None:
        self._semestre = semestre

    def is_es_oficial(self) -> bool:
        return self._es_oficial

    def set_es_oficial(self, es_oficial: bool) -> None:
        self._es_oficial = es_oficial

    def __str__(self):
        c1, c2, c3 = self._cortes["corte1"], self._cortes["corte2"], self._cortes["corte3"]
        cortes_str = f" [C1:{c1:.1f} C2:{c2:.1f} C3:{c3:.1f}]" if any(c > 0 for c in (c1, c2, c3)) else ""
        return f"[{self._id}] {self._nombre} (Semestre {self._semestre}) - Créditos: {self._creditos} - Nota Final: {self._nota:.1f}{cortes_str}"
