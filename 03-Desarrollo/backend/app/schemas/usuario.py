from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    correo: EmailStr


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8, max_length=100)
    rol: str = Field(default="usuario", pattern="^(administrador|usuario)$")


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    correo: Optional[EmailStr] = None
    rol: Optional[str] = Field(None, pattern="^(administrador|usuario)$")
    activo: Optional[bool] = None


class UsuarioInDB(UsuarioBase):
    id: UUID
    rol: str
    activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True


class UsuarioResponse(UsuarioInDB):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None
    rol: Optional[str] = None