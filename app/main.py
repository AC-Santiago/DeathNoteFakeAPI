from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.connection import create_all_tables
from app.utils.http_error_handler import HTTPErrorHandler


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield


app = FastAPI(
    title="Death Note API",
    description="API for managing the Death Note",
    version="0.0.1",
    lifespan=lifespan,
)

app.add_middleware(HTTPErrorHandler)
