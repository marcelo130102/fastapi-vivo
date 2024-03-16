# import pytest

# from app import app


# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# def test_holamundo(client):
#     response = client.get('/')
#     print(response)
#     assert response.status_code == 200
#     assert response.json == {"message": "Hello World"}

# def test_saludo(client):
#     response = client.get('/saludo/pepe')
#     assert response.status_code == 200
#     assert response.json == {"message": "Hello pepe"}

# def test_saludo_error(client):
#     response = client.get('/saludo/')
#     assert response.status_code == 404
#     assert response.json == {"message": "Not found"}