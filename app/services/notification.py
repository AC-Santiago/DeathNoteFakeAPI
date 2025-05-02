from typing import Dict, Set, Literal
from fastapi import WebSocket


class NotificationManager:
    """Gestor de conexiones WebSocket para notificaciones en tiempo real"""

    def __init__(self):
        self.connections: Dict[str, Set[WebSocket]] = {
            "deaths": set(),
            "status_updates": set(),
        }

    async def connect(
        self,
        websocket: WebSocket,
        channel: Literal["deaths", "status_updates"] = "deaths",
    ):
        """Establece una nueva conexión WebSocket"""
        await websocket.accept()
        self.connections[channel].add(websocket)

    async def disconnect(
        self,
        websocket: WebSocket,
        channel: Literal["deaths", "status_updates"] = "deaths",
    ):
        """Cierra y elimina una conexión WebSocket"""
        if websocket in self.connections[channel]:
            self.connections[channel].remove(websocket)

    async def broadcast_death(self, persona_data: Dict):
        """Envía una notificación de muerte a todos los clientes conectados"""
        message = {
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
        await self._broadcast_to_channel("deaths", message)

        await self.broadcast_status_update("person_updated", persona_data)

    async def broadcast_status_update(self, event: str, persona_data: Dict):
        """Envía una actualización de estado a todos los clientes conectados"""
        message = {"event": event, "data": persona_data}
        await self._broadcast_to_channel("status_updates", message)

    def _format_dates_in_dict(self, data: Dict) -> Dict:
        """Formatea todas las fechas en el diccionario al formato estándar"""
        if isinstance(data, dict):
            for key, value in data.items():
                if hasattr(value, "strftime"):
                    data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(value, dict):
                    data[key] = self._format_dates_in_dict(value)
        return data

    async def _broadcast_to_channel(self, channel: str, message: Dict):
        """Método interno para enviar mensajes a un canal específico"""
        disconnected = set()

        if "data" in message:
            message["data"] = self._format_dates_in_dict(message["data"])

        for connection in self.connections[channel]:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(
                    f"Error sending message to client: {e}, in channel: {channel}"
                )
                disconnected.add(connection)

        for connection in disconnected:
            await self.disconnect(connection, channel)


notification_manager = NotificationManager()
