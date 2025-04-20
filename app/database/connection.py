import os
from typing import Annotated, AsyncGenerator

from fastapi import Depends
import firebase_admin
from firebase_admin import credentials, firestore_async
from google.cloud.firestore import AsyncClient

from app.core.config import get_settings

settings = get_settings()


def connect_firebase():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    firebase_key = settings.FIRE_BASE_KEY.strip('"').strip("'")
    path = os.path.join(base_dir, "app", "json", firebase_key)
    path = f"/DeathNoteFake{path}"
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"El archivo de credenciales no existe en: {path}"
        )

    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred)


async def get_client() -> AsyncGenerator[AsyncClient, None]:
    if not firebase_admin._apps:
        connect_firebase()
    client = firestore_async.client()
    yield client


FirebaseClient = Annotated[AsyncClient, Depends(get_client)]
