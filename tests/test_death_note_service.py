import pytest
from unittest.mock import AsyncMock, patch
from app.services.death_note import (
    schedule_death,
    _execute_death,
    _cancel_scheduled_death,
    _check_if_person_is_dead,
)
from app.schemas.persona import CausaMuerte, EstadoPersona


@pytest.mark.asyncio
async def test_execute_death(mock_db, sample_persona_data):
    mock_doc_ref = AsyncMock()
    updated_data = {**sample_persona_data, "estado": EstadoPersona.MUERTO}
    mock_doc_ref.get = AsyncMock(
        return_value=AsyncMock(to_dict=lambda: updated_data)
    )
    mock_db.collection().document.return_value = mock_doc_ref

    await _execute_death(mock_db, "test-id")

    mock_doc_ref.update.assert_called_once()
    update_data = mock_doc_ref.update.call_args[0][0]
    assert update_data["estado"] == EstadoPersona.MUERTO


@pytest.mark.asyncio
async def test_schedule_death(mock_db, sample_persona_data):
    causa_muerte = CausaMuerte(causa="Test Death", detalles="Test Details")

    with patch(
        "app.services.death_note._execute_death_with_delay"
    ) as mock_execute:
        await schedule_death(mock_db, "test-id", causa_muerte)

        mock_execute.assert_called_once()


def test_cancel_scheduled_death():
    persona_id = "test-id"

    result = _cancel_scheduled_death(persona_id)

    assert result is False


def test_check_if_person_is_dead():
    persona_viva = {"estado": EstadoPersona.VIVO}
    assert not _check_if_person_is_dead(persona_viva)

    persona_muerta = {"estado": EstadoPersona.MUERTO}
    assert _check_if_person_is_dead(persona_muerta)
