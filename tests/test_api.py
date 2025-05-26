from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_api_initalization():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '"hello world"'
