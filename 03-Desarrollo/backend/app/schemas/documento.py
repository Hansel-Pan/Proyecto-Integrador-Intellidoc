from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class DocumentoBase(BaseModel):
    nombre_archivo: str = Field(..., min_length=1, max_length=255)
    formato: str = Field(..., pattern="^(pdf|docx|txt)$")
    ruta_almacenamiento: str = Field(..., min_length=1, max_length=500)


class DocumentoCreate(DocumentoBase):
    repositorio_id: UUID


class DocumentoUpdate(BaseModel):
    categoria: Optional[str] = Field(None, max_length=50)
    resumen: Optional[str] = None
    campos_extraidos: Optional[Dict[str, Any]] = None
    estado: Optional[str] = Field(None, pattern="^(pendiente|procesando|procesado|error)$")


class DocumentoInDB(DocumentoBase):
    id: UUID
    repositorio_id: UUID
    usuario_carga_id: UUID
    estado: str
    categoria: Optional[str] = None
    resumen: Optional[str] = None
    campos_extraidos: Optional[Dict[str, Any]] = None
    creado_en: datetime
    procesado_en: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentoResponse(DocumentoInDB):
    pass


class DocumentoListResponse(BaseModel):
    id: UUID
    nombre_archivo: str
    formato: str
    estado: str
    categoria: Optional[str] = None
    creado_en: datetime

    class Config:
        from_attributes = True


class DocumentoSearchResult(BaseModel):
    id: UUID
    nombre_archivo: str
    formato: str
    categoria: Optional[str] = None
    resumen: Optional[str] = None
    repositorio_nombre: str
    coincidencias: List[str] = []

    class Config:
        from_attributes = True