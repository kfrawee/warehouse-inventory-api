from fastapi import APIRouter
from app.api.routers import ping
from app.api.routers import device

api_router = APIRouter()

# Include additional routers here
api_router.include_router(ping.router)
api_router.include_router(device.router)
