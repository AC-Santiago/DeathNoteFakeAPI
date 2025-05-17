import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.crud.persona import (
    create_person,
    get_people,
    get_person,
    update_person,
)
from app.schemas.persona import EstadoPersona


@pytest.mark.asyncio
async def test_create_person_success(mock_db, persona_create_data):
    """Test exitoso de creación de persona."""
    foto_url = "./fotos/example1.jpg"

    mock_doc_ref = mock_db.collection("personas").document()
    mock_doc_ref.set = AsyncMock()

    result = await create_person(mock_db, persona_create_data, foto_url)

    assert result is not None
    assert result["nombre"] == persona_create_data.nombre
    assert result["apellido"] == persona_create_data.apellido
    assert result["edad"] == persona_create_data.edad
    assert result["estado"] == EstadoPersona.VIVO
    assert result["foto_url"] == foto_url

    mock_doc_ref.set.assert_called_once()


@pytest.mark.asyncio
async def test_get_people_success(mock_db):
    """Test exitoso de obtención de lista de personas."""
    mock_personas = [
        {"nombre": "Light", "apellido": "Yagami", "edad": 17},
        {"nombre": "L", "apellido": "Lawliet", "edad": 24},
        {"nombre": "Misa", "apellido": "Amane", "edad": 19},
    ]

    mock_docs = []
    for persona in mock_personas:
        persona_data = persona.copy()
        mock_doc = AsyncMock(to_dict=MagicMock(return_value=persona_data))
        mock_docs.append(mock_doc)

    async def async_iter():
        for doc in mock_docs:
            yield doc

    mock_collection = mock_db.collection("personas")
    mock_query = AsyncMock()
    mock_collection.limit = MagicMock(return_value=mock_query)
    mock_query.offset = MagicMock(return_value=mock_query)
    mock_query.stream = async_iter

    result = await get_people(mock_db)

    assert len(result) == len(mock_personas)

    expected_personas = {
        (persona["nombre"], persona["apellido"], persona["edad"])
        for persona in mock_personas
    }
    result_personas = {
        (persona["nombre"], persona["apellido"], persona["edad"])
        for persona in result
    }

    assert expected_personas == result_personas


@pytest.mark.asyncio
async def test_get_person_success(mock_db, sample_persona_data):
    """Test exitoso de obtención de una persona."""
    persona_id = "test-id"

    mock_doc = AsyncMock(to_dict=MagicMock(return_value=sample_persona_data))
    mock_doc.exists = True
    mock_db.collection().document().get.return_value = mock_doc

    result = await get_person(mock_db, persona_id)

    assert result is not None
    assert result == sample_persona_data
    mock_db.collection().document.assert_called_with(persona_id)


@pytest.mark.asyncio
async def test_get_person_not_found(mock_db):
    """Test de obtención de una persona que no existe."""
    persona_id = "non-existent-id"

    mock_doc = AsyncMock()
    mock_doc.exists = False
    mock_db.collection().document().get.return_value = mock_doc

    result = await get_person(mock_db, persona_id)

    assert result is None


@pytest.mark.asyncio
async def test_update_person_success(mock_db, sample_persona_data):
    """Test exitoso de actualización de persona."""
    persona_id = "test-id"
    update_data = {"edad": 18}
    updated_data = {**sample_persona_data, **update_data}

    mock_doc_ref = mock_db.collection().document()
    mock_doc_ref.update = AsyncMock()
    mock_doc = AsyncMock(to_dict=MagicMock(return_value=updated_data))
    mock_doc.exists = True
    mock_doc_ref.get.return_value = mock_doc

    result = await update_person(mock_db, persona_id, update_data)

    assert result is not None
    assert result["edad"] == update_data["edad"]
    mock_doc_ref.update.assert_called_once_with(update_data)


@pytest.mark.asyncio
async def test_update_person_not_found(mock_db):
    """Test de actualización de una persona que no existe."""
    persona_id = "non-existent-id"
    update_data = {"edad": 18}

    mock_doc_ref = mock_db.collection().document()
    mock_doc_ref.update = AsyncMock()
    mock_doc = AsyncMock()
    mock_doc.exists = False
    mock_doc_ref.get.return_value = mock_doc

    result = await update_person(mock_db, persona_id, update_data)

    assert result is None


@pytest.mark.asyncio
async def test_crud_operations_error_handling(mock_db, persona_create_data):
    """Test del manejo de errores en las operaciones CRUD."""
    mock_db.collection().document().set.side_effect = Exception(
        "Database error"
    )

    with pytest.raises(HTTPException) as exc_info:
        await create_person(
            mock_db, persona_create_data, "./fotos/example1.jpg"
        )
    assert exc_info.value.status_code == 500
    assert "Error al crear la persona" in str(exc_info.value.detail)

    mock_collection = MagicMock()
    mock_db.collection.return_value = mock_collection

    mock_limit = MagicMock()
    mock_collection.limit.return_value = mock_limit

    mock_offset = MagicMock()
    mock_limit.offset.return_value = mock_offset

    async def error_stream():
        raise Exception("Database error")
        yield

    mock_offset.stream = error_stream

    with pytest.raises(HTTPException) as exc_info:
        await get_people(mock_db)
    assert exc_info.value.status_code == 500
    assert "Error al obtener las personas" in str(exc_info.value.detail)

    mock_db.collection().document().get.side_effect = Exception(
        "Database error"
    )
    with pytest.raises(HTTPException) as exc_info:
        await get_person(mock_db, "test-id")
    assert exc_info.value.status_code == 500
    assert "Error al obtener la persona" in str(exc_info.value.detail)

    mock_db.collection().document().update.side_effect = Exception(
        "Database error"
    )
    with pytest.raises(HTTPException) as exc_info:
        await update_person(mock_db, "test-id", {"edad": 18})
    assert exc_info.value.status_code == 500
    assert "Error al actualizar la persona" in str(exc_info.value.detail)
