from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field


class RepositorioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)


class RepositorioCreate(RepositorioBase):
    pass


class RepositorioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)


class RepositorioInDB(RepositorioBase):
    id: UUID
    usuario_creador_id: UUID
    creado_en: datetime

    class Config:
        from_attributes = True


class RepositorioResponse(RepositorioInDB):
    pass


class RepositorioWithStats(RepositorioInDB):
    total_documentos: int = 0
    documentos_por_estado: dict = {}
    documentos_por_categoria: dict = {}