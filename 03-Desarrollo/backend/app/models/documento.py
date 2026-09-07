import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import String, Text, DateTime, ForeignKey, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.types import GUID


class Documento(Base):
    __tablename__ = "documentos"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    repositorio_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("repositorios.id", ondelete="CASCADE"), nullable=False
    )
    usuario_carga_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    nombre_archivo: Mapped[str] = mapped_column(String(255), nullable=False)
    formato: Mapped[str] = mapped_column(String(10), nullable=False)
    ruta_almacenamiento: Mapped[str] = mapped_column(String(500), nullable=False)
    estado: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pendiente", index=True
    )
    categoria: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    resumen: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    campos_extraidos: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    procesado_en: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    repositorio: Mapped["Repositorio"] = relationship(back_populates="documentos")
    usuario_carga: Mapped["Usuario"] = relationship(
        back_populates="documentos_cargados", foreign_keys=[usuario_carga_id]
    )
    fragmentos: Mapped[list["Fragmento"]] = relationship(
        back_populates="documento", cascade="all, delete-orphan", order_by="Fragmento.orden"
    )
    logs: Mapped[list["LogProcesamiento"]] = relationship(
        back_populates="documento", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Documento(id={self.id}, nombre={self.nombre_archivo}, estado={self.estado})>"