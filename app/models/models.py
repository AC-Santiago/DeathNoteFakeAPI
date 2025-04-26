from uuid import UUID, uuid4

from app.schemas.persona import EstadoPersona, PersonaCreate
from pydantic import Field


class Persona(PersonaCreate):
    uid: UUID = Field(default_factory=uuid4)

    def to_dict(self) -> dict:
        return {
            "uid": str(self.uid),
            "nombre": self.nombre,
            "apellido": self.apellido,
            "edad": self.edad,
            "estado": (
                self.estado.value
                if isinstance(self.estado, EstadoPersona)
                else self.estado
            ),
            "foto_url": self.foto_url,
            "causa_muerte": (
                self.causa_muerte.model_dump() if self.causa_muerte else None
            ),
            "fecha_registro": self.fecha_registro.isoformat(),
        }
