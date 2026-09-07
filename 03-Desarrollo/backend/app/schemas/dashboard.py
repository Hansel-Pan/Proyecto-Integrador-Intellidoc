from datetime import datetime
from uuid import UUID
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_documentos: int
    documentos_por_categoria: Dict[str, int]
    documentos_por_estado: Dict[str, int]
    ultimos_errores: List["LogProcesamientoResumen"]


class LogProcesamientoResumen(BaseModel):
    id: UUID
    documento_id: UUID
    nombre_archivo: str
    tipo: str
    mensaje: str
    creado_en: datetime


class DashboardStats(BaseModel):
    total_repositorios: int
    total_documentos: int
    total_usuarios: int
    documentos_por_categoria: Dict[str, int]
    documentos_por_estado: Dict[str, int]
    errores_recientes: List[LogProcesamientoResumen]