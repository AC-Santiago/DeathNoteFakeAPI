from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from google.cloud.firestore import AsyncClient

from app.models.models import Persona, PersonaCreate
from app.schemas.persona import EstadoPersona


async def create_persona(
    db: AsyncClient, persona_data: PersonaCreate, foto_url: Optional[str] = None
) -> dict:
    """
    Crea una nueva persona en la base de datos.

    Args:
        db: Cliente de Firestore
        persona_data: Datos de la persona a crear
        foto_url: URL de la foto de la persona

    Returns:
        dict: Datos de la persona creada

    Raises:
        HTTPException: Si no se proporciona una foto
    """
    if not foto_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere una foto para registrar a la persona",
        )

    try:
        persona = Persona(
            nombre=persona_data.nombre,
            apellido=persona_data.apellido,
            edad=persona_data.edad,
            estado=EstadoPersona.VIVO,
            foto_url=foto_url,
            fecha_registro=datetime.now(timezone.utc),
        )

        doc_id = str(persona.uid)
        doc_ref = db.collection("personas").document(doc_id)
        persona_dict = persona.to_dict()
        await doc_ref.set(persona_dict)

        return persona_dict

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la persona: {str(e)}",
        )
