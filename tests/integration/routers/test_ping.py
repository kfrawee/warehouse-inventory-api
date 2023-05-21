from http import HTTPStatus

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data["active"] is True
    assert "current_time" in response_data
