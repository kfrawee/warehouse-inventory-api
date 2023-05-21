from http import HTTPStatus

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_configure_device_success(seeded_device):
    response = client.patch(f"/service/configure/{seeded_device.uuid}")

    assert response.status_code == HTTPStatus.ACCEPTED

    # Assert the response content
    response_data = response.json()
    assert "message" in response_data
    assert "device" in response_data

    # Assert the device status and temperature
    device = response_data["device"]
    assert device["status"] == "ACTIVE"
    assert 0 <= device["temperature"] <= 10

    # configure again
    response = client.patch(f"/service/configure/{seeded_device.uuid}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_configure_device_not_found(seeded_device):
    response = client.patch(f"/service/configure/{seeded_device.uuid}xx")

    assert response.status_code == HTTPStatus.NOT_FOUND
