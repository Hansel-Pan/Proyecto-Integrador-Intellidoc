import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.types import GUID


class Repositorio(Base):
    __tablename__ = "repositorios"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    usuario_creador_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    creador: Mapped["Usuario"] = relationship(back_populates="repositorios")
    documentos: Mapped[list["Documento"]] = relationship(
        back_populates="repositorio", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Repositorio(id={self.id}, nombre={self.nombre})>"