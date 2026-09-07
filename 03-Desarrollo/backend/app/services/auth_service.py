from uuid import UUID
from sqlalchemy.orm import Session

from app.models import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import verify_password, get_password_hash, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate(self, correo: str, password: str) -> Usuario | None:
        user = self.db.query(Usuario).filter(Usuario.correo == correo).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def create_user(self, user_in: UsuarioCreate) -> Usuario:
        existing = self.db.query(Usuario).filter(Usuario.correo == user_in.correo).first()
        if existing:
            raise ValueError("El correo ya está registrado")
        
        user = Usuario(
            nombre=user_in.nombre,
            correo=user_in.correo,
            password_hash=get_password_hash(user_in.password),
            rol=user_in.rol,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: UUID) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == user_id).first()

    def get_user_by_email(self, correo: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.correo == correo).first()

    def update_user(self, user_id: UUID, user_in: UsuarioUpdate) -> Usuario | None:
        user = self.get_user(user_id)
        if not user:
            return None
        
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: UUID) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    def create_token(self, user: Usuario) -> str:
        return create_access_token(data={"sub": str(user.id), "rol": user.rol})