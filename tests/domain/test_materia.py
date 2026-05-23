import pytest
from domain.materia import Materia


# Creamos un objeto (materia) para las pruebas
# Las pruebas unitarias se realizan con el patron AAA (Arrange - Act - Assert)

def test_creacion_materia():
    materia = Materia(101, "Calculo Univariado", 4, 1)

    assert materia.get_id() == 101
    assert materia.get_nombre() == "Calculo Univariado"
    assert materia.get_creditos() == 4
    assert materia.get_semestre() == 1
    assert materia.get_nota() == 0.0
    assert materia.is_es_oficial() == True


# Setters y Getters

def test_set_nombre():
    materia = Materia(101, "Calculo Univariado", 4, 1) # creamos una materia con este nombre
    materia.set_nombre("Algoritmos y Fundamentos de Programación") # la cambio por esta
    assert materia.get_nombre() == "Algoritmos y Fundamentos de Programación" # verifico el nuevo


def test_set_creditos():
    materia = Materia(101, "Calculo Univariado", 4, 1) # creo una materia con 4 creditos
    materia.set_creditos(3) # cambio los creditos a 3
    assert materia.get_creditos() == 3 # verifico que realmente sean 3  


def test_set_semestre():
    materia = Materia(101, "Calculo Univariado", 4, 1)
    materia.set_semestre(4) #cambio semestre a 4
    assert materia.get_semestre() == 4 #verifico que el semestre si sea 4


def test_set_es_oficial():
    materia = Materia(101, "Calculo Unviariado", 4, 1)
    materia.set_es_oficial(False) #lo cambio a que la amteria no es oficial
    assert materia.is_es_oficial() is False #verifico que si sea false


# Notas

def test_set_nota_valida():
    materia = Materia(101, "Calculo Univariado", 4, 1)
    materia.set_nota(3.2)
    assert materia.get_nota() == 3.2


def test_set_nota_invalida():
    materia = Materia(101, "Calculo Univariado", 4, 1)
    with pytest.raises(ValueError): #verifica la nota invalida y lanza un ValuError
        materia.set_nota(6.0)


# Cortes

def test_set_notas_cortes():
    materia = Materia(101, "Calculo Univariado", 4, 1) #creo la materia
    materia.set_notas_cortes(4.0, 3.0, 5.0) #creo los cortes simulados
    cortes = materia.get_cortes() #guardo en el diccionario los cortes

    #verifico que cada corte si corresponda
    assert cortes["corte1"] == 4.0
    assert cortes["corte2"] == 3.0
    assert cortes["corte3"] == 5.0

    #verifico que la nota si se calculo bien con -> (4*0.3)+(3*0.3)+(5*0.4)
    assert materia.get_nota() == 4.1


def test_set_notas_cortes_invalidas():
    materia = Materia(101, "Calculo Univariado", 4, 1)

    with pytest.raises(ValueError):
        materia.set_notas_cortes(4.0, 8.0, 5.0)


# Funcion str

def test_str_sin_cortes():
    materia = Materia(101, "Calculo Univariado", 4, 1) #creo la materia
    resultado = str(materia) #casteo el objeto a texto

    #verifico resultados
    assert "Calculo Univariado" in resultado 
    assert "Nota Final: 0.0" in resultado 


def test_str_con_cortes():
    materia = Materia(101, "Calculo Univariado", 4, 1)
    materia.set_notas_cortes(4.0, 4.0, 5.0) #asigno notas por corte
    resultado = str(materia) #casteo el objeto a texto

    #verifico resultados
    assert "C1:4.0" in resultado
    assert "C2:4.0" in resultado
    assert "C3:5.0" in resultado