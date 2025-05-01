from typing import Optional

from fastapi import HTTPException, status
from google.cloud.firestore import AsyncClient

from app.models.models import Persona, PersonaCreate
from app.schemas.persona import EstadoPersona


async def create_person(
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


async def get_people(
    db: AsyncClient, limit: int = 10, offset: int = 0
) -> list[dict]:
    """
    Obtiene una lista de personas de la base de datos.
    Args:
        db: Cliente de Firestore
        limit: Número máximo de personas a obtener
        offset: Número de personas a omitir
    Returns:
        list[dict]: Lista de personas
    """
    try:
        query = db.collection("personas").limit(limit).offset(offset)
        docs = []
        async for doc in query.stream():
            docs.append(doc.to_dict())
        return docs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las personas: {str(e)}",
        )


async def get_person(db: AsyncClient, persona_id: str) -> Optional[dict]:
    """
    Obtiene una persona de la base de datos por su ID.
    Args:
        db: Cliente de Firestore
        persona_id: ID de la persona a obtener
    Returns:
        Optional[dict]: Datos de la persona o None si no se encuentra
    """
    try:
        doc_ref = db.collection("personas").document(persona_id)
        doc = await doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la persona: {str(e)}",
        )


async def update_person(
    db: AsyncClient, persona_id: str, persona_data: dict
) -> Optional[dict]:
    """
    Actualiza una persona en la base de datos por su ID.
    Args:
        db: Cliente de Firestore
        persona_id: ID de la persona a actualizar
        persona_data: Datos de la persona a actualizar

    """
    try:
        doc_ref = db.collection("personas").document(persona_id)
        await doc_ref.update(persona_data)
        updated_doc = await doc_ref.get()
        return updated_doc.to_dict() if updated_doc.exists else None

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la persona: {str(e)}",
        )
