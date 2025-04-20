from uuid import UUID, uuid4

from app.schemas.persona import PersonaCreate
from pydantic import Field


class Persona(PersonaCreate):
    uid: UUID = Field(default_factory=uuid4)

    def to_dict(self) -> dict:
        return {
            "uid": str(self.uid),
            "nombre": self.nombre,
            "apellido": self.apellido,
            "edad": self.edad,
            "estado": self.estado,
        }
