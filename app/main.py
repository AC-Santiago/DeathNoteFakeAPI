from contextlib import asynccontextmanager
import cloudinary
from fastapi import FastAPI

from app.core.config import Settings
from app.database.connection import connect_firebase
from app.routers import persona
from app.utils.http_error_handler import HTTPErrorHandler


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_firebase()
    settings = Settings()
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
    )
    yield


app = FastAPI(
    title="Death Note API",
    description="API for managing the Death Note",
    version="0.0.1",
    lifespan=lifespan,
)

app.add_middleware(HTTPErrorHandler)
app.include_router(persona.router, tags=["personas"])
