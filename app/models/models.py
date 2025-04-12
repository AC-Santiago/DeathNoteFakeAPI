from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EstadoPersona(str, Enum):
    VIVO = "vivo"
    MUERTO = "muerto"


class Persona(BaseModel):
    nombre: str
    apellido: str
    edad: Optional[int] = None
    estado: EstadoPersona
