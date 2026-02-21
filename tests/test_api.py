
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_api_initialization():
    """
    Test the initizalization of the FastAPI app
    """

    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '"I\'m alive!"'
