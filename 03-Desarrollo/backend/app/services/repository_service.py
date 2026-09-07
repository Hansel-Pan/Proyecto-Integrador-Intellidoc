from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models import Repositorio, Usuario
from app.schemas.repositorio import RepositorioCreate, RepositorioUpdate


class RepositoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_repositorio(self, repositorio_in: RepositorioCreate, usuario_creador_id: UUID) -> Repositorio:
        repositorio = Repositorio(
            nombre=repositorio_in.nombre,
            usuario_creador_id=usuario_creador_id,
        )
        self.db.add(repositorio)
        self.db.commit()
        self.db.refresh(repositorio)
        return repositorio

    def get_repositorio(self, repositorio_id: UUID) -> Optional[Repositorio]:
        return self.db.query(Repositorio).filter(Repositorio.id == repositorio_id).first()

    def get_repositorios_by_user(
        self, 
        usuario_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Repositorio]:
        return self.db.query(Repositorio).filter(
            Repositorio.usuario_creador_id == usuario_id
        ).order_by(Repositorio.creado_en.desc()).offset(skip).limit(limit).all()

    def get_all_repositorios(self, skip: int = 0, limit: int = 100) -> List[Repositorio]:
        return self.db.query(Repositorio).order_by(Repositorio.creado_en.desc()).offset(skip).limit(limit).all()

    def update_repositorio(self, repositorio_id: UUID, repositorio_in: RepositorioUpdate) -> Optional[Repositorio]:
        repositorio = self.get_repositorio(repositorio_id)
        if not repositorio:
            return None
        
        update_data = repositorio_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(repositorio, field, value)
        
        self.db.commit()
        self.db.refresh(repositorio)
        return repositorio

    def delete_repositorio(self, repositorio_id: UUID) -> bool:
        repositorio = self.get_repositorio(repositorio_id)
        if not repositorio:
            return False
        self.db.delete(repositorio)
        self.db.commit()
        return True

    def count_repositorios_by_user(self, usuario_id: UUID) -> int:
        return self.db.query(Repositorio).filter(Repositorio.usuario_creador_id == usuario_id).count()