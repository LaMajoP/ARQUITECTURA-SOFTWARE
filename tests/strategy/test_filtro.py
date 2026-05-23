from strategy.filtro_strategy import FiltroIngles, FiltroElectivas
from domain.materia import Materia



def crear_materia(id, nombre, creditos=4, semestre=1):
    return Materia(id, nombre, creditos, semestre)



def test_filtro_ingles():

    # arrange
    m1 = crear_materia(103, "Matemáticas Discretas")
    m2 = crear_materia(104, "Introducción a Sistemas Inteligentes")
    m3 = crear_materia(107, "Inglés I")

    materias = [m1, m2, m3]
    filtro = FiltroIngles()

    # act
    resultado = filtro.filtrar(materias)

    # assert
    nombres = [m.get_nombre() for m in resultado]

    assert "Introducción a Sistemas Inteligentes" in nombres
    assert "Matemáticas Discretas" in nombres

    assert "Inglés I" not in nombres
    assert len(resultado) == 2




def test_filtro_electivas():

    m1 = crear_materia(103, "Matemáticas Discretas")
    m2 = crear_materia(104, "Introducción a Sistemas Inteligentes")
    m3 = crear_materia(605, "Electiva I")

    materias = [m1, m2, m3]
    filtro = FiltroElectivas()

    resultado = filtro.filtrar(materias)

    nombres = [m.get_nombre() for m in resultado]

    assert "Introducción a Sistemas Inteligentes" in nombres
    assert "Matemáticas Discretas" in nombres
    assert "Electiva I" not in nombres

    assert len(resultado) == 2




def test_filtro_lista_vacia():

    filtro = FiltroElectivas()
    resultado = filtro.filtrar([])
    assert resultado == []