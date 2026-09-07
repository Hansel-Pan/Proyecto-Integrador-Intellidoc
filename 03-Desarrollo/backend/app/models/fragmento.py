import uuid
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.types import GUID


class Fragmento(Base):
    __tablename__ = "fragmentos"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    documento_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("documentos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    vector_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    orden: Mapped[int] = mapped_column(Integer, nullable=False)

    documento: Mapped["Documento"] = relationship(back_populates="fragmentos")

    def __repr__(self) -> str:
        return f"<Fragmento(id={self.id}, documento_id={self.documento_id}, orden={self.orden})>"