import asyncio
from typing import Optional
from google.cloud.firestore import AsyncClient
from app.crud.persona import get_person, update_person
from app.schemas.persona import CausaMuerte, EstadoPersona
from app.services.notification import notification_manager


async def execute_death(
    db: AsyncClient, persona_id: str, causa_muerte: Optional[CausaMuerte] = None
):
    """
    Ejecuta la muerte de una persona según las reglas de Death Note.
    """
    try:
        persona = await get_person(db, persona_id)
        if not persona:
            return

        if not causa_muerte:
            causa_muerte = CausaMuerte(
                causa="Ataque al corazón",
                detalles="Muerte por defecto de la Death Note",
            )
        causa_muerte_dict_copy = causa_muerte.model_copy().model_dump().copy()
        date_format = causa_muerte_dict_copy["fecha_registro"].strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        persona["estado"] = EstadoPersona.MUERTO
        persona["causa_muerte"] = causa_muerte.model_dump()

        updated_persona = await update_person(db, persona_id, persona)

        update_persona_copy = updated_persona.copy()
        update_persona_copy["causa_muerte"]["fecha_registro"] = date_format
        updated_persona["causa_muerte"] = update_persona_copy["causa_muerte"]

        await notification_manager.broadcast_death(updated_persona)
    except Exception as e:
        print(f"Error ejecutando la muerte: {str(e)}")


async def schedule_death(
    db: AsyncClient, persona_id: str, causa_muerte: Optional[CausaMuerte] = None
):
    """
    Programa la muerte de una persona según las reglas de Death Note.

    Si no se especifica causa_muerte, la persona morirá de un ataque al corazón
    después de 40 segundos.

    Si se especifica causa_muerte, la persona morirá según los detalles
    especificados después de 40 segundos + 6 minutos y 40 segundos adicionales
    si se proporcionaron detalles.
    """
    if causa_muerte and causa_muerte.detalles:
        delay = 400 + 40  # segundos
    else:
        delay = 40

    asyncio.create_task(
        execute_death_with_delay(db, persona_id, causa_muerte, delay)
    )


async def execute_death_with_delay(
    db: AsyncClient,
    persona_id: str,
    causa_muerte: Optional[CausaMuerte],
    delay: int,
):
    """
    Ejecuta la muerte después del tiempo especificado.
    """
    await asyncio.sleep(delay)
    await execute_death(db, persona_id, causa_muerte)
