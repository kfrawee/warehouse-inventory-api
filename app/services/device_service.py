from random import randint

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Device
from app.database.config import get_db
from app.models import DeviceConfigure, DeviceStatus

router = APIRouter(prefix="/service", tags=["Device Service"])


@router.patch(
    "/configure/{uuid}",
    response_model=DeviceConfigure,
    status_code=status.HTTP_202_ACCEPTED,
)
def configure_device(uuid: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.uuid == uuid).one_or_none()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with uuid '{uuid}' not found",
        )

    if device.status == DeviceStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Device with uuid '{uuid}' is already configured",
        )

    device.status = DeviceStatus.ACTIVE
    device.temperature = randint(0, 10)

    db.commit()
    db.refresh(device)

    return {"message": "Device configured successfully", "device": device}
