from enum import Enum
from pydantic import BaseModel


class EstadoPersona(str, Enum):
    VIVO = "vivo"
    MUERTO = "muerto"


class PersonaCreate(BaseModel):
    nombre: str
    apellido: str
    edad: int
    estado: EstadoPersona = EstadoPersona.VIVO
