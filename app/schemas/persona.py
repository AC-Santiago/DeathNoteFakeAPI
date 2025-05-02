from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class EstadoPersona(str, Enum):
    VIVO = "vivo"
    MUERTO = "muerto"


class CausaMuerteBase(BaseModel):
    causa: str = Field(..., description="Causa de la muerte")
    detalles: Optional[str] = Field(
        None, description="Detalles específicos de la muerte"
    )


class CausaMuerte(CausaMuerteBase):
    fecha_registro: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class PersonaBase(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre de la persona")
    apellido: str = Field(
        ..., min_length=1, description="Apellido de la persona"
    )
    edad: int = Field(..., gt=0, lt=150, description="Edad de la persona")


class PersonaRequest(PersonaBase):
    pass


class PersonaCreate(PersonaBase):
    estado: EstadoPersona = Field(default=EstadoPersona.VIVO)
    foto_url: Optional[str] = None
    causa_muerte: Optional[CausaMuerte] = None
    fecha_registro: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class PersonaDeathRequest(BaseModel):
    persona_id: str = Field(..., description="ID de la persona que ha muerto")
    causa_muerte: CausaMuerteBase = Field(..., description="Causa de la muerte")
