from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.orm import Session

from app.database import Device
from app.database.config import get_db
from app.models import DeviceCreate, DeviceRead, DeviceUpdate, DevicesRead, DeviceStatus

router = APIRouter(prefix="/device", tags=["Device"])


@router.post("/", response_model=DeviceRead, status_code=http_status.HTTP_201_CREATED)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    new_device = Device(
        pin_code=device.pin_code, status=device.status, temperature=device.temperature
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


# apply pagination
@router.get("/", response_model=DevicesRead, status_code=http_status.HTTP_200_OK)
def get_devices(
    db: Session = Depends(get_db),
    status: Optional[DeviceStatus] = None,
    next_token: Optional[str] = None,
    limit: int = 5,
):
    query = db.query(Device)

    if status:
        query = query.filter(Device.status == status)

    query = query.order_by(Device.created_at)
    total = query.count()

    if next_token:
        next_token_device = query.filter(Device.uuid == next_token).first()
        if not next_token_device:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Invalid next token",
            )
        query = query.filter(Device.id > next_token_device.id)

    devices = query.limit(limit).all()
    next_token = devices[-1].uuid if len(devices) == limit else None

    return {
        "count": len(devices),
        "total": total,
        "next_token": next_token,
        "devices": devices,
    }


@router.get("/{uuid}", response_model=DeviceRead)
def get_device_by_pin(uuid: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.uuid == uuid).one_or_none()
    if not device:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Device with uuid '{uuid}' not found",
        )
    return device


@router.put("/{uuid}", response_model=DeviceRead)
def update_device(uuid: str, device: DeviceUpdate, db: Session = Depends(get_db)):
    existing_device = db.query(Device).filter(Device.uuid == uuid).one_or_none()
    if not existing_device:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Device with uuid '{uuid}' not found",
        )
    if device.pin_code:
        existing_device.pin_code = device.pin_code
    if device.status:
        existing_device.status = device.status
    if device.temperature:
        existing_device.temperature = device.temperature
    db.commit()
    db.refresh(existing_device)
    return existing_device


@router.delete("/{uuid}", status_code=http_status.HTTP_204_NO_CONTENT)
def delete_device(uuid: str, db: Session = Depends(get_db)):
    existing_device = db.query(Device).filter(Device.uuid == uuid).one_or_none()
    if not existing_device:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Device with uuid '{uuid}' not found",
        )

    db.delete(existing_device)
    db.commit()
