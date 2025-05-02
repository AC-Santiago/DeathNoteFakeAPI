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

        if check_if_person_is_dead(persona):
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
    cancel_scheduled_death(persona_id)
    perona = await get_person(db, persona_id)
    if not perona:
        raise ValueError(
            f"No se encontró la persona con ID {persona_id} para programar la muerte."
        )
    if check_if_person_is_dead(perona):
        raise ValueError(
            f"La persona con ID {persona_id} ya está muerta. No se puede programar la muerte."
        )
    if causa_muerte:
        delay = 400
    else:
        delay = 40
    if causa_muerte and causa_muerte.detalles:
        delay = 40
    task = asyncio.create_task(
        execute_death_with_delay(db, persona_id, causa_muerte, delay)
    )

    _scheduled_deaths[persona_id] = task


_scheduled_deaths = {}


async def execute_death_with_delay(
    db: AsyncClient,
    persona_id: str,
    causa_muerte: Optional[CausaMuerte],
    delay: int,
):
    """
    Ejecuta la muerte después del tiempo especificado.
    """
    try:
        await asyncio.sleep(delay)
        await execute_death(db, persona_id, causa_muerte)
    finally:
        if persona_id in _scheduled_deaths:
            del _scheduled_deaths[persona_id]


def cancel_scheduled_death(persona_id: str) -> bool:
    """
    Cancela una muerte programada si existe.
    Retorna True si se canceló una muerte, False si no había ninguna programada.
    """
    if persona_id in _scheduled_deaths:
        task = _scheduled_deaths[persona_id]
        task.cancel()
        del _scheduled_deaths[persona_id]
        return True
    return False


def check_if_person_is_dead(persona: dict) -> bool:
    """
    Verifica si la persona está muerta.
    """
    if persona["estado"] == EstadoPersona.MUERTO:
        return True
    return False
