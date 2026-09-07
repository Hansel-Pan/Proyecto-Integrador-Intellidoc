import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Text, DateTime, ForeignKey, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.types import GUID


class ConsultaChat(Base):
    __tablename__ = "consultas_chat"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    pregunta: Mapped[str] = mapped_column(Text, nullable=False)
    respuesta: Mapped[str] = mapped_column(Text, nullable=False)
    documentos_fuente: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSON, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    usuario: Mapped["Usuario"] = relationship(back_populates="consultas_chat")

    def __repr__(self) -> str:
        return f"<ConsultaChat(id={self.id}, usuario_id={self.usuario_id})>"