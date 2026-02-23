from infrastructure.i_malla_loader import IMallaLoader
from domain.malla_curricular import MallaCurricular

class CSVMallaLoader(IMallaLoader):
    def load(self, path: str) -> MallaCurricular:
        raise NotImplementedError("La carga desde CSV aún no está implementada.")
