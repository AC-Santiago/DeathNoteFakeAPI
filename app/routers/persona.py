from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from google.cloud.firestore import AsyncClient

from app.crud.persona import create_persona
from app.database.connection import get_client
from app.models.models import Persona
from app.schemas.persona import PersonaCreate

router = APIRouter()


@router.post(
    "/persona", status_code=status.HTTP_201_CREATED, response_model=Persona
)
async def create_persona_endpoint(
    db: Annotated[AsyncClient, Depends(get_client)], new_persona: PersonaCreate
):
    try:
        persona_dict = await create_persona(db, new_persona)
        return persona_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
