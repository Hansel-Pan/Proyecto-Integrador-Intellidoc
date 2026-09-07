import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.types import GUID


class LogProcesamiento(Base):
    __tablename__ = "logs_procesamiento"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    documento_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("documentos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    mensaje: Mapped[str] = mapped_column(Text, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    documento: Mapped["Documento"] = relationship(back_populates="logs")

    def __repr__(self) -> str:
        return f"<LogProcesamiento(id={self.id}, tipo={self.tipo}, documento_id={self.documento_id})>"