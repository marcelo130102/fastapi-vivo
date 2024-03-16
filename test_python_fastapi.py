import pytest
from fastapi.testclient import TestClient
from main import app
from requests.auth import HTTPBasicAuth

# Instalar
# pytest
# requests
# httpx

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_holamundo(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_login(client):
    response = client.post("/login", auth=HTTPBasicAuth("admin", "password"))
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}
    assert response.cookies.get("session")
    session_cookie = response.cookies.get("session")

    response = client.get("/secure", cookies={"session_token": session_cookie})
    assert response.status_code == 200
    assert response.json() == {"message": "Secure content"}

    response = client.get("/logout", cookies={"session_token": session_cookie})
    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful"}
    assert not response.cookies.get("session_token")

    response = client.get("/secure", cookies={"session_token": session_cookie})
    assert response.status_code == 401