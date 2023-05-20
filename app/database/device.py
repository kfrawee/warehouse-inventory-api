from uuid import uuid4

from sqlalchemy import Column, Enum, Integer, String

from app.database import TimestampMixin
from app.database.config import Base
from app.models.device import DeviceStatus


class Device(TimestampMixin, Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True, index=True)
    # create unique uuid
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    pin_code = Column(Integer, unique=False, nullable=False)
    status = Column(Enum(DeviceStatus), default=DeviceStatus.READY)
    temperature = Column(Integer, nullable=False, default=-1)
