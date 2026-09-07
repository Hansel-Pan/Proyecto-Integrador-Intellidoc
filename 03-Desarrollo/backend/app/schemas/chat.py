from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    pregunta: str = Field(..., min_length=1, max_length=2000)
    repositorio_id: Optional[UUID] = None


class FuenteDocumento(BaseModel):
    documento_id: UUID
    nombre_archivo: str
    fragmento_texto: str
    similitud: float


class ChatResponse(BaseModel):
    respuesta: str
    fuentes: List[FuenteDocumento] = []


class ConsultaChatInDB(BaseModel):
    id: UUID
    usuario_id: UUID
    pregunta: str
    respuesta: str
    documentos_fuente: Optional[List[Dict[str, Any]]] = None
    creado_en: datetime

    class Config:
        from_attributes = True