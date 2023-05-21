import pytest
from pytest import fixture
from random import randint, choice
from app.database import Device
from app.database.config import get_db, initialize_database


@fixture(scope="function")
def seeded_device():
    db = next(get_db())
    initialize_database()

    session = db()
    device_data = {"pin_code": 1234567, "status": "READY", "temperature": -1}
    device = Device(**device_data)
    session.add(device)

    session.commit()
    session.flush()

    yield device

    with session.begin_nested():
        session.query(Device).filter(Device.id == device.id).delete()

    session.close()


@fixture
def seeded_devices():
    db = next(get_db())
    initialize_database()
    session = db()

    devices = []

    for _ in range(10):
        device_data = {
            "pin_code": randint(1000000, 9999999),
            "status": choice(["ACTIVE", "READY"]),
            "temperature": randint(-1, 10),
        }
        device = Device(**device_data)
        session.add(device)
        devices.append(device)

        session.commit()
        session.flush()

    yield devices

    with session.begin_nested():
        for device in devices:
            session.query(Device).filter(Device.id == device.id).delete()

    session.close()
