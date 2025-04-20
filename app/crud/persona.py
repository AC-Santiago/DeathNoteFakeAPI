from google.cloud.firestore import AsyncClient

from app.models.models import Persona, PersonaCreate


async def create_persona(db: AsyncClient, persona_data: PersonaCreate):
    persona = Persona(**persona_data.model_dump())
    try:
        doc_id = str(persona.uid)
        doc_ref = db.collection("personas").document(doc_id)
        persona_dict = persona.to_dict()
        await doc_ref.set(persona_dict)
        doc = await doc_ref.get()
        if doc.exists:
            return persona_dict
        raise Exception("El documento no se creó correctamente")
    except Exception as e:
        raise Exception(f"Error al crear la persona: {e}") from e
