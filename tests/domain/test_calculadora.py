
import pytest
from domain.materia import Materia
from domain.calculadora_promedio import CalculadoraPromedio
# from strategy.filtro_strategy import FiltroIngles, FiltroElectivas
import pytest


# funcion auxiliar para crear una materia
def crear_materia(id, nombre, creditos, semestre, nota):
    materia = Materia(id, nombre, creditos, semestre)
    materia.set_nota(nota)
    return materia



def test_calcular_promedio_ponderado():

    # arrange
    m1 = crear_materia(101, "Cálculo Univariado", 4, 1, 3.4)
    m2 = crear_materia(102, "Algoritmos y Fundamentos de Programación", 4, 1, 4.1)
    materias = [m1, m2]
    calculadora = CalculadoraPromedio()

    # act
    promedio = calculadora.calcular(materias)

    # assert
    esperado = ((3.4 * 4) + (4.1 * 4)) / (4 + 4)

    assert promedio == esperado # verifico que el promedio calculado sea igual al esperado


# test lista vacia (se prueba el caso en donde la lista de materias esta vacia)
def test_calcular_lista_vacia():
    calculadora = CalculadoraPromedio()
    promedio = calculadora.calcular([])
    assert promedio == 0.0




def test_calcular_creditos_cero():
    # arrange
    m1 = crear_materia(101, "Cálculo Univariado", 0, 1, 3.4)
    m2 = crear_materia(102, "Algoritmos y Fundamentos de Programación", 0, 1, 4.1)
    materias = [m1, m2]

    calculadora = CalculadoraPromedio()

    #act
    promedio = calculadora.calcular(materias)

    # assert
    assert promedio == 0.0




def test_calcular_por_semestre():

    #arrange
    m1 = crear_materia(101, "Cálculo Univariado", 4, 1, 3.2)
    m2 = crear_materia(102, "Algoritmos y Fundamentos de Programación", 4, 1, 4.1)
    m3 = crear_materia(103, "Matemáticas Discretas", 2, 2, 3.9)

    materias = [m1, m2, m3]

    calculadora = CalculadoraPromedio()

    # act
    promedio = calculadora.calcular_por_semestre(materias, 1)

    #assert
    esperado = ((3.2 * 4) + (4.1 * 4)) / (4 + 4)

    assert promedio == esperado



# mock del filtro strategy (simula la funcion del flitro)
class MockFiltro:

    def filtrar(self, materias):
        return [m for m in materias if m.get_nota() >= 3.0] #filtra por nota




def test_calcular_con_filtro():
    # arrange
    m1 = crear_materia(101, "Cálculo Univariado", 4, 1, 3.2)
    m2 = crear_materia(102, "Algoritmos y Fundamentos de Programación", 4, 1, 4.1)

    materias = [m1, m2]

    calculadora = CalculadoraPromedio()

    filtro = MockFiltro()

    calculadora.set_filtro(filtro)

    # act
    promedio = calculadora.calcular(materias)

    # assert
    assert promedio == 3.65