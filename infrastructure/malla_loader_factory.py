from infrastructure.i_malla_loader import IMallaLoader
from infrastructure.json_malla_loader import JSONMallaLoader
from infrastructure.csv_malla_loader import CSVMallaLoader

class MallaLoaderFactory:
    @staticmethod
    def get_loader(extension: str) -> IMallaLoader:
        ext = extension.lower()
        if ext == 'json':
            return JSONMallaLoader()
        elif ext == 'csv':
            return CSVMallaLoader()
        else:
            raise ValueError(f"Formato de archivo no soportado: {extension}")
