import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from google.cloud.firestore import AsyncClient
from google.cloud.firestore_v1.document import DocumentSnapshot
from google.cloud.firestore_v1.collection import CollectionReference
from app.schemas.persona import PersonaCreate, EstadoPersona
from uuid import UUID


class MockDocumentSnapshot:
    def __init__(self, data=None, exists=True):
        self._data = data or {}
        self._exists = exists

    def to_dict(self):
        return self._data

    @property
    def exists(self):
        return self._exists


@pytest.fixture
def mock_db():
    """Fixture que proporciona un mock de AsyncClient de Firestore."""
    mock_client = AsyncMock()

    # Mock para collection
    mock_collection = AsyncMock()
    mock_client.collection = MagicMock(return_value=mock_collection)

    # Mock para document
    mock_doc_ref = AsyncMock()
    mock_collection.document = MagicMock(return_value=mock_doc_ref)

    # Mock para get
    mock_doc_ref.get.return_value = MockDocumentSnapshot(exists=True)

    return mock_client


@pytest.fixture
def sample_persona_data():
    """Fixture que proporciona datos de ejemplo para una persona."""
    return {
        "nombre": "Light",
        "apellido": "Yagami",
        "edad": 17,
        "estado": EstadoPersona.VIVO,
        "foto_url": "http://example.com/foto.jpg",
    }


@pytest.fixture
def persona_create_data(sample_persona_data):
    """Fixture que proporciona un objeto PersonaCreate con datos de ejemplo."""
    return PersonaCreate(**sample_persona_data)
