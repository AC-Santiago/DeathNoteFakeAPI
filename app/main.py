from fastapi import FastAPI

from app.utils.http_error_handler import HTTPErrorHandler

app = FastAPI()

app.add_middleware(HTTPErrorHandler)
