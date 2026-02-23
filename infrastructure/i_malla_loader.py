from abc import ABC, abstractmethod
from domain.malla_curricular import MallaCurricular

class IMallaLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> MallaCurricular:
        pass
