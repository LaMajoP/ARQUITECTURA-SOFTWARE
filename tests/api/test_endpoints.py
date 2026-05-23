from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)




def login_admin(username= "admin", password= "admin123"):
    response = client.post(
        "/login",
        json={
            "username": username,
            "password": password
        }
    )

    return response.json()["access_token"]

def login_student(username= "student", password= "student456"):
    response = client.post(
        "/login",
        json={
            "username": username,
            "password": password
        }
    )

    return response.json()["access_token"]


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def materia(
    id=101,
    nombre="Cálculo Univariado",
    creditos=4,
    semestre=1,
    nota=4.0
):
    return {
        "id": id,
        "nombre": nombre,
        "creditos": creditos,
        "semestre": semestre,
        "nota": nota,
        "es_oficial": True
    }



#login

def test_login_ok():

    response = client.post(
        "/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalido():

    response = client.post(
        "/login",
        json={
            "username": "admin",
            "password": "mal"
        }
    )

    assert response.status_code == 401


#promedio
def test_promedio():

    token = login_admin()

    response = client.post(
        "/promedio",
        headers=auth_headers(token),
        json={
            "materias": [
                materia(101, "Cálculo Univariado", 4, 1, 4.0),
                materia(102, "Algoritmos y Fundamentos de Programación", 4, 1, 3.5)
            ]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "promedio_calculado" in data


def test_promedio_sin_token():

    response = client.post(
        "/promedio",
        json={"materias": []}
    )

    assert response.status_code in [401, 403]



#promedio objetivo
def test_promedio_objetivo_admin():

    token = login_admin("admin", "admin123")

    response = client.post(
        "/promedio-objetivo",
        headers=auth_headers(token),
        json={
            "materias_cursadas": [materia(101, "Cálculo Univariado", 4, 1, 3.5)],
            "materias_pendientes": [materia(102, "Física", 4, 2, 0.0)], 
            "promedio_objetivo": 4.0 
        }
    )

    assert response.status_code == 200


def test_promedio_objetivo_student():

    token = login_student("student", "student456")

    response = client.post(
        "/promedio-objetivo",
        headers=auth_headers(token),
        json={
            "promedio_actual": 3.5,
            "promedio_objetivo": 4.0,
            "creditos_aprobados": 40,
            "pendientes": []
        }
    )

    assert response.status_code == 403