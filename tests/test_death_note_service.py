import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from datetime import datetime, timedelta

from app.services.death_note import (
    schedule_death,
    _execute_death,
    _execute_death_with_delay,
    _cancel_scheduled_death,
    _check_if_person_is_dead,
)
from app.schemas.persona import EstadoPersona, CausaMuerte


@pytest.fixture
def mock_notification_manager():
    with patch("app.services.death_note.notification_manager") as mock:
        mock.broadcast_death = AsyncMock()
        mock.broadcast_status_update = AsyncMock()
        yield mock


@pytest.mark.asyncio
async def test_execute_death_success(
    mock_db, mock_notification_manager, sample_persona_data
):
    """Test exitoso de ejecución de muerte."""
    # Preparar los datos de prueba
    persona_id = "test-id"
    causa_muerte = CausaMuerte(
        causa="Ataque al corazón",
        detalles="Muerte instantánea",
        fecha_registro=datetime.now(),
    )

    # Preparar el mock de la persona viva
    persona_viva = {
        **sample_persona_data,
        "uid": persona_id,
        "estado": EstadoPersona.VIVO,
    }

    # Mock para get_person
    with patch("app.services.death_note.get_person") as mock_get_person:
        mock_get_person.return_value = persona_viva

        # Mock para update_person
        with patch(
            "app.services.death_note.update_person"
        ) as mock_update_person:
            # Preparar el resultado esperado después de la actualización
            expected_updated_persona = {
                **persona_viva,
                "estado": EstadoPersona.MUERTO,
                "causa_muerte": causa_muerte.model_dump(),
            }
            mock_update_person.return_value = expected_updated_persona

            # Ejecutar la función
            await _execute_death(mock_db, persona_id, causa_muerte)

            # Verificar que get_person fue llamado correctamente
            mock_get_person.assert_called_once_with(mock_db, persona_id)

            # Verificar que update_person fue llamado con los datos correctos
            mock_update_person.assert_called_once()
            actual_update_data = mock_update_person.call_args.args[2]

            assert actual_update_data["estado"] == EstadoPersona.MUERTO
            assert isinstance(actual_update_data["causa_muerte"], dict)
            assert (
                actual_update_data["causa_muerte"]["causa"]
                == causa_muerte.causa
            )
            assert (
                actual_update_data["causa_muerte"]["detalles"]
                == causa_muerte.detalles
            )

            # Verificar que las notificaciones fueron enviadas
            mock_notification_manager.broadcast_death.assert_called_once()
            mock_notification_manager.broadcast_status_update.assert_not_called()  # Esta no debería ser llamada según el código actual


@pytest.mark.asyncio
async def test_schedule_death_success(mock_db, sample_persona_data):
    """Test exitoso de programación de muerte."""
    persona_id = "test-id"
    causa_muerte = CausaMuerte(
        causa="Ataque al corazón",
        detalles="Muerte instantánea",
        fecha_registro=datetime.now(),
    )

    # Preparar el mock de la persona viva
    persona_viva = {
        **sample_persona_data,
        "uid": persona_id,
        "estado": EstadoPersona.VIVO,
    }

    # Mock get_person para simular que la persona existe
    with patch("app.services.death_note.get_person") as mock_get_person:
        mock_get_person.return_value = persona_viva

        with patch(
            "app.services.death_note._execute_death_with_delay"
        ) as mock_execute:
            mock_execute.return_value = None
            await schedule_death(mock_db, persona_id, causa_muerte)
            mock_execute.assert_called_once_with(
                mock_db, persona_id, causa_muerte, pytest.approx(40, abs=1)
            )


@pytest.mark.asyncio
async def test_execute_death_with_delay(mock_db, mock_notification_manager):
    """Test de ejecución de muerte con delay."""
    persona_id = "test-id"
    delay = 1
    causa_muerte = CausaMuerte(
        causa="Ataque al corazón",
        detalles="Muerte instantánea",
        fecha_registro=datetime.now(),
    )

    with patch("asyncio.sleep") as mock_sleep:
        mock_sleep.return_value = None
        await _execute_death_with_delay(
            mock_db, persona_id, causa_muerte, delay
        )
        mock_sleep.assert_called_once_with(delay)


@pytest.mark.asyncio
async def test_cancel_scheduled_death_success():
    """Test exitoso de cancelación de muerte programada."""
    persona_id = "test-id"

    # Simular una muerte programada
    with patch(
        "app.services.death_note._scheduled_deaths", {persona_id: MagicMock()}
    ):
        result = _cancel_scheduled_death(persona_id)
        assert result is True


@pytest.mark.asyncio
async def test_cancel_scheduled_death_not_found():
    """Test de cancelación de muerte no programada."""
    persona_id = "non-existent-id"

    result = _cancel_scheduled_death(persona_id)
    assert result is False
