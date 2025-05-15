import pytest
from fastapi.testclient import TestClient
from google.cloud.firestore import AsyncClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.schemas.persona import EstadoPersona


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
async def mock_db():
    mock_client = AsyncMock(spec=AsyncClient)

    async def mock_get_client():
        yield mock_client

    with patch("app.database.connection.get_client", mock_get_client):
        yield mock_client


@pytest.fixture
def sample_persona_data():
    return {
        "nombre": "Light",
        "apellido": "Yagami",
        "edad": 17,
        "estado": EstadoPersona.VIVO,
        "foto_url": None,
        "causa_muerte": None,
    }


@pytest.fixture
def sample_death_request():
    return {
        "persona_id": "test-id",
        "causa_muerte": {"causa": "Heart Attack", "detalles": "Death Note"},
    }
