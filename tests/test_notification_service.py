import pytest
from fastapi import WebSocket
from unittest.mock import AsyncMock
from app.services.notification import NotificationManager
from datetime import datetime


@pytest.fixture
def notification_manager():
    return NotificationManager()


@pytest.fixture
def mock_websocket():
    websocket = AsyncMock(spec=WebSocket)
    return websocket


def test_notification_manager_init(notification_manager):
    assert hasattr(notification_manager, "active_connections")
    assert isinstance(notification_manager.active_connections, dict)
    assert "deaths" in notification_manager.active_connections
    assert "status_updates" in notification_manager.active_connections


@pytest.mark.asyncio
async def test_connect(notification_manager, mock_websocket):
    await notification_manager.connect(mock_websocket)

    assert mock_websocket in notification_manager.active_connections["deaths"]

    await notification_manager.connect(mock_websocket, "status_updates")

    assert (
        mock_websocket
        in notification_manager.active_connections["status_updates"]
    )


@pytest.mark.asyncio
async def test_disconnect(notification_manager, mock_websocket):
    await notification_manager.connect(mock_websocket)

    await notification_manager.disconnect(mock_websocket)

    assert (
        mock_websocket not in notification_manager.active_connections["deaths"]
    )


@pytest.mark.asyncio
async def test_broadcast_death(notification_manager, mock_websocket):
    # Conectar un websocket
    await notification_manager.connect(mock_websocket)

    persona_data = {
        "nombre": "Test",
        "apellido": "User",
        "fecha_muerte": datetime.now(),
    }

    await notification_manager.broadcast_death(persona_data)

    mock_websocket.send_json.assert_called_once()

    call_args = mock_websocket.send_json.call_args[0][0]
    assert "event" in call_args
    assert call_args["event"] == "death"
    assert "data" in call_args


@pytest.mark.asyncio
async def test_broadcast_status_update(notification_manager, mock_websocket):
    await notification_manager.connect(mock_websocket, "status_updates")

    persona_data = {"nombre": "Test", "apellido": "User", "estado": "MUERTO"}

    await notification_manager.broadcast_status_update(
        "status_change", persona_data
    )

    mock_websocket.send_json.assert_called_once()

    call_args = mock_websocket.send_json.call_args[0][0]
    assert "event" in call_args
    assert call_args["event"] == "status_change"
    assert "data" in call_args
