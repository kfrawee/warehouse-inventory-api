from fastapi import APIRouter
from app.services import device_service

services_router = APIRouter()

# Include additional routers here
services_router.include_router(device_service.router)
