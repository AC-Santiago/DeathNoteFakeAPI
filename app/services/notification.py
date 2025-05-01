from typing import Dict, Set
from fastapi import WebSocket


class NotificationManager:
    """Gestor de conexiones WebSocket para notificaciones en tiempo real"""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """Establece una nueva conexión WebSocket"""
        await websocket.accept()
        self.active_connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        """Cierra y elimina una conexión WebSocket"""
        self.active_connections.remove(websocket)

    async def broadcast_death(self, persona_data: Dict):
        """Envía una notificación de muerte a todos los clientes conectados"""
        disconnected = set()

        for connection in self.active_connections:
            try:
                await connection.send_json(
                    {
                        "event": "death_notification",
                        "data": {
                            "persona_id": persona_data.get("uid"),
                            "nombre": persona_data.get("nombre"),
                            "apellido": persona_data.get("apellido"),
                            "causa_muerte": persona_data.get(
                                "causa_muerte",
                                {
                                    "causa": "Ataque al corazón",
                                    "detalles": "Muerte por defecto de la Death Note",
                                },
                            ),
                        },
                    }
                )
            except Exception as e:
                print(f"Error sending message to client: {e}")
                disconnected.add(connection)

        for connection in disconnected:
            self.active_connections.remove(connection)


notification_manager = NotificationManager()
