from http import HTTPStatus

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_device_success(seeded_device):
    response = client.get(f"/device/{seeded_device.uuid}")

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()

    assert response_data.get("uuid") == seeded_device.uuid
    assert response_data.get("pin_code") == seeded_device.pin_code


def test_get_device_not_found(seeded_device):
    response = client.get(f"/device/{seeded_device.uuid}xx")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_device(seeded_device):
    updated_device_data = {"status": "ACTIVE"}
    response = client.put(f"/device/{seeded_device.uuid}", json=updated_device_data)
    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.json()["status"] == updated_device_data["status"]


def test_delete_device(seeded_device):
    response = client.delete(f"/device/{seeded_device.uuid}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_create_device_error():
    new_device_data = {"pin_code": "1234"}
    response = client.post("/device", json=new_device_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# TEST FULL FLOW
def test_create_device():
    new_device_data = {"pin_code": 1234567, "status": "ACTIVE", "temperature": 0}

    # CREATE
    response = client.post("/device", json=new_device_data)
    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()
    assert response_data.get("pin_code") == new_device_data["pin_code"]
    assert response_data.get("status") == new_device_data["status"]
    assert response_data.get("temperature") == new_device_data["temperature"]
    assert response_data.get("uuid")

    device_uuid = response_data.get("uuid")

    # GET
    response = client.get(f"/device/{device_uuid}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["uuid"] == device_uuid

    # UPDATE
    updated_device_data = {"status": "READY", "temperature": -1}
    response = client.put(f"/device/{device_uuid}", json=updated_device_data)
    assert response.status_code == HTTPStatus.ACCEPTED

    response_data = response.json()

    assert response_data.get("status") == updated_device_data["status"]
    assert response_data.get("temperature") == updated_device_data["temperature"]
    assert response_data.get("uuid") == device_uuid

    # DELETE
    response = client.delete(f"/device/{device_uuid}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_devices(seeded_devices):
    response = client.get("/device")
    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert response_data.get("count") == 5
    print(response_data)
    assert response_data.get("devices")
    assert response_data.get("next_token")
