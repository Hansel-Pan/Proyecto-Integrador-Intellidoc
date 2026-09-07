from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user, require_admin
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate, Token, UsuarioInDB
from app.services.auth_service import AuthService
from app.models import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token)
def login(
    correo: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    user = auth_service.authenticate(correo, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.activo:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    access_token = auth_service.create_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(
    nombre: str = Form(...),
    correo: str = Form(...),
    password: str = Form(...),
    rol: str = Form("usuario"),
    db: Session = Depends(get_db),
):
    """Registro público - primer usuario se convierte en admin automáticamente"""
    auth_service = AuthService(db)
    
    # Verificar si es el primer usuario
    user_count = db.query(Usuario).count()
    if user_count == 0:
        # Primer usuario = administrador
        rol = "administrador"
    
    user_in = UsuarioCreate(nombre=nombre, correo=correo, password=password, rol=rol)
    
    try:
        user = auth_service.create_user(user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=UsuarioInDB)
def read_users_me(
    current_user: Usuario = Depends(get_current_active_user),
):
    return current_user


@router.put("/me", response_model=UsuarioResponse)
def update_user_me(
    user_in: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    auth_service = AuthService(db)
    user = auth_service.update_user(current_user.id, user_in)
    return user


@router.get("/users", response_model=list[UsuarioResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    auth_service = AuthService(db)
    users = db.query(Usuario).offset(skip).limit(limit).all()
    return users


@router.post("/users", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    auth_service = AuthService(db)
    try:
        user = auth_service.create_user(user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/{user_id}", response_model=UsuarioResponse)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    from uuid import UUID
    auth_service = AuthService(db)
    user = auth_service.get_user(UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.put("/users/{user_id}", response_model=UsuarioResponse)
def update_user(
    user_id: str,
    user_in: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    from uuid import UUID
    auth_service = AuthService(db)
    user = auth_service.update_user(UUID(user_id), user_in)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    from uuid import UUID
    auth_service = AuthService(db)
    if not auth_service.delete_user(UUID(user_id)):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")