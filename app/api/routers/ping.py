from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])


@router.get("/ping")
def ping():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"active": True, "current_time": current_time}
