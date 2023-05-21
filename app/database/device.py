from uuid import uuid4

from sqlalchemy import Column, Enum, Integer, String

from app.database import TimestampMixin
from app.database.config import Base
from app.models.device import DeviceStatus


class Device(TimestampMixin, Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    pin_code = Column(Integer, unique=False, nullable=False)
    status = Column(Enum(DeviceStatus), default=DeviceStatus.READY)
    temperature = Column(Integer, nullable=False, default=-1)

    def __repr__(self):
        return f"<Device(uuid={self.uuid}, pin_code={self.pin_code}, status={self.status}, temperature={self.temperature})>"
