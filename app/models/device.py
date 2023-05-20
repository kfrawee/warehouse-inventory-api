from fastapi import HTTPException, status
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, conint, validator


class DeviceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    READY = "READY"


class Device(BaseModel):
    pin_code: conint(ge=1000000, lt=10000000) = Field(
        ..., description="Unique secret seven-digit pin code", example=1234567
    )
    status: DeviceStatus = Field(
        default=DeviceStatus.READY, description="Device status", example="ACTIVE"
    )
    temperature: int = Field(
        ge=-1, le=10, default=-1, description="Temperature", example=5.0
    )


class DeviceStatusTemp(BaseModel):
    status: DeviceStatus = Field(
        default=DeviceStatus.READY, description="Device status", example="ACTIVE"
    )
    temperature: int = Field(
        ge=-1, le=10, default=-1, description="Temperature", example=5.0
    )

    @validator("temperature")
    def validate_temperature(cls, temperature, values):
        if values.get("status") == DeviceStatus.ACTIVE and not (0 <= temperature <= 10):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Temperature must be between 0 and 10 for an ACTIVE device",
            )
        return temperature


class DeviceCreate(DeviceStatusTemp, Device):
    pass


class DeviceUpdate(DeviceStatusTemp):
    pin_code: conint(ge=1000000, lt=10000000) = Field(
        default=None, description="Unique secret seven-digit pin code", example=1234567
    )


class DeviceRead(Device):
    uuid: str = Field(
        ..., description="Device uuid", example="1a2b3c4d-5e6f-7g8h-9i0j-k1l2m3n4o5p"
    )
    created_at: datetime = Field(
        ..., description="Device creation date", example="2023-05-20 17:38:18"
    )
    updated_at: datetime = Field(
        ..., description="Device update date", example="2023-05-20 17:38:18"
    )

    class Config:
        orm_mode = True


class DevicesRead(BaseModel):
    count: int = Field(..., description="Devices count", example=1)
    total: int = Field(..., description="Devices total", example=1)
    next_token: str = Field(default=None, description="Next token; Device UUID")
    devices: list[DeviceRead]

    class Config:
        orm_mode = True


class DeviceConfigure(BaseModel):
    message: str = Field(
        ..., description="Message", example="Device configured successfully"
    )
    device: DeviceRead
