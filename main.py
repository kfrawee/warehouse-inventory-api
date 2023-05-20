import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api import api_router
from app.services import services_router
from app.database.config import initialize_database


async def internal_server_error_handler(request: Request, exc: Exception):
    # Custom error handling logic
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal Server Error"},
    )


app = FastAPI()
app.exception_handlers[Exception] = internal_server_error_handler

# Initialize the database
initialize_database()

# Register routers
app.include_router(api_router)
app.include_router(services_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
