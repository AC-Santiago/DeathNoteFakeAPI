import asyncio
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

from app.crud.persona import create_person, get_people
from app.database.connection import get_client
from app.models.models import Persona
from app.schemas.persona import EstadoPersona, PersonaCreate, PersonaRequest
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

    try:
        await notification_manager.connect(websocket)
        while True:
            try:
                await websocket.send_json({"event": "ping"})
                await asyncio.sleep(10)
                # await websocket.receive_text()
            except Exception:
                break
    except Exception:
        pass
    finally:
        await notification_manager.disconnect(websocket)


@router.post(
    "/persona",
    status_code=status.HTTP_201_CREATED,
    response_model=Persona,
    description="Registra una nueva persona en la Death Note",
)
async def create_persona_endpoint(
    db: Annotated[AsyncClient, Depends(get_client)],
    nombre: str = Body(..., description="Nombre de la persona"),
    apellido: str = Body(..., description="Apellido de la persona"),
    edad: int = Body(..., gt=0, lt=150, description="Edad de la persona"),
    foto: UploadFile = File(...),
):
    """
    Registra una nueva persona en la Death Note.
    Requiere nombre, apellido, edad y una foto.
    """
    try:
        persona_request = PersonaRequest(
            nombre=nombre, apellido=apellido, edad=edad
        )
        foto_url = await upload_photo(foto)
        new_persona = PersonaCreate(
            nombre=persona_request.nombre,
            apellido=persona_request.apellido,
            edad=persona_request.edad,
            foto_url=foto_url,
            estado=EstadoPersona.VIVO,
            causa_muerte=None,
        )
        persona_dict = await create_person(db, new_persona, foto_url)
        await schedule_death(db, persona_dict["uid"])
        return persona_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/persona/death")
async def death_persona_endpoint(
    db: Annotated[AsyncClient, Depends(get_client)],
    persona_id: str = Body(..., description="ID de la persona"),
    causa_muerte: dict = Body(
        ..., description="Causa de la muerte de la persona"
    ),
):
    """
    Marca a una persona como muerta en la Death Note.
    Requiere el ID de la persona y la causa de la muerte.
    """
    try:
        await schedule_death(db, persona_id, causa_muerte)
        return {"message": "Persona marcada como muerta"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get(
    "/personas",
    status_code=status.HTTP_200_OK,
    response_model=list[Persona],
    description="Obtiene una lista de personas registradas en la Death Note",
)
async def get_personas_endpoint(
    db: Annotated[AsyncClient, Depends(get_client)],
    limit: int = 10,
    offset: int = 0,
):
    """
    Obtiene una lista de personas registradas en la Death Note.
    """
    try:
        personas = await get_people(db, limit, offset)
        return personas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
