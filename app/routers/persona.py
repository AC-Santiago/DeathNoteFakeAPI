from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    HTTPException,
    UploadFile,
    WebSocket,
    status,
)
from google.cloud.firestore import AsyncClient

from app.crud.persona import (
    create_persona,
)
from app.database.connection import get_client
from app.models.models import Persona
from app.schemas.persona import PersonaCreate
from app.services.death_note import schedule_death
from app.services.notification import notification_manager
from app.services.storage import upload_photo

router = APIRouter()


@router.websocket("/ws/deaths")
async def websocket_deaths(websocket: WebSocket):
    """
    Endpoint WebSocket para recibir notificaciones en tiempo real de las muertes.

    Los clientes recibirán un mensaje JSON cada vez que una persona muera, con el formato:
    {
        "event": "death_notification",
        "data": {
            "persona_id": "uuid",
            "nombre": "string",
            "apellido": "string",
            "causa_muerte": {
                "causa": "string",
                "detalles": "string"
            }
        }
    }
    """
    await notification_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        await notification_manager.disconnect(websocket)


@router.post(
    "/persona",
    status_code=status.HTTP_201_CREATED,
    response_model=Persona,
    description="Registra una nueva persona en la Death Note",
)
async def create_persona_endpoint(
    db: Annotated[AsyncClient, Depends(get_client)],
    new_persona: PersonaCreate = Body(...),
    foto: UploadFile = File(...),
):
    """
    Registra una nueva persona en la Death Note.
    Requiere nombre, apellido, edad y una foto.
    """
    try:
        foto_url = await upload_photo(foto)
        persona_dict = await create_persona(db, new_persona, foto_url)
        await schedule_death(db, persona_dict["uid"])

        return persona_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
