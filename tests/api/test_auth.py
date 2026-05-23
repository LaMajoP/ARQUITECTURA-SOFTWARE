#import pytest
from fastapi.testclient import TestClient
from api.main import app


# cliente que simula llamadas HTTP sin levantar el servidor real
client = TestClient(app)


# prueba para el login exitoso
def test_login_exitoso():

    # arrange
    credenciales = {"username": "admin", "password": "admin123"}

    # act
    response = client.post("/login", json=credenciales)

    # assert
    assert response.status_code == 200                        # debe responder OK
    assert "access_token" in response.json()                  # debe retornar el token
    assert response.json()["token_type"] == "bearer"          # tipo de token correcto


# prueba para la contraseña incorrecta

def test_login_contrasena_incorrecta():

    # arrange
    credenciales = {"username": "admin", "password": "contrasena_incorrecta"}

    # act
    response = client.post("/login", json=credenciales)

    # assert
    assert response.status_code == 401                        # debe rechazar la solicitud


def test_login_usuario_inexistente():

    # arrange
    credenciales = {"username": "usuario_falso", "password": "1234"}

    # act
    response = client.post("/login", json=credenciales)

    # assert
    assert response.status_code == 401                        # usuario no existe, debe rechazar


def test_login_student_exitoso():

    # arrange
    credenciales = {"username": "student", "password": "student456"}

    # act
    response = client.post("/login", json=credenciales)

    # assert
    assert response.status_code == 200
    assert "access_token" in response.json()