import pytest
from unittest.mock import AsyncMock
from app.crud.persona import (
    create_person,
    get_people,
    get_person,
    update_person,
)
from app.schemas.persona import PersonaCreate


@pytest.mark.asyncio
async def test_create_person(mock_db, sample_persona_data):
    mock_doc_ref = AsyncMock()
    mock_doc_ref.get = AsyncMock(
        return_value=AsyncMock(to_dict=lambda: sample_persona_data)
    )
    mock_db.collection().document.return_value = mock_doc_ref

    persona_data = PersonaCreate(**sample_persona_data)
    result = await create_person(mock_db, persona_data)

    assert result is not None
    assert result["nombre"] == sample_persona_data["nombre"]
    assert result["apellido"] == sample_persona_data["apellido"]
    assert result["edad"] == sample_persona_data["edad"]


@pytest.mark.asyncio
async def test_get_people(mock_db):
    test_people = [
        {"nombre": "Light", "apellido": "Yagami", "edad": 17},
        {"nombre": "L", "apellido": "Lawliet", "edad": 24},
    ]

    mock_docs = [AsyncMock(to_dict=lambda: person) for person in test_people]
    mock_db.collection().limit().offset().stream = AsyncMock(
        return_value=mock_docs
    )

    result = await get_people(mock_db)

    assert len(result) == len(test_people)
    assert all(isinstance(person, dict) for person in result)


@pytest.mark.asyncio
async def test_get_person(mock_db, sample_persona_data):
    mock_doc = AsyncMock(to_dict=lambda: sample_persona_data)
    mock_db.collection().document().get = AsyncMock(return_value=mock_doc)

    result = await get_person(mock_db, "test-id")

    assert result is not None
    assert result["nombre"] == sample_persona_data["nombre"]
    assert result["apellido"] == sample_persona_data["apellido"]


@pytest.mark.asyncio
async def test_update_person(mock_db, sample_persona_data):
    update_data = {"edad": 18}

    updated_data = {**sample_persona_data, **update_data}
    mock_doc_ref = AsyncMock()
    mock_doc_ref.get = AsyncMock(
        return_value=AsyncMock(to_dict=lambda: updated_data)
    )
    mock_db.collection().document.return_value = mock_doc_ref

    result = await update_person(mock_db, "test-id", update_data)

    assert result is not None
    assert result["edad"] == update_data["edad"]
