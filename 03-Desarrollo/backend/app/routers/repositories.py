from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user, require_admin
from app.schemas.repositorio import RepositorioCreate, RepositorioUpdate, RepositorioResponse, RepositorioWithStats
from app.services.repository_service import RepositoryService
from app.services.document_service import DocumentService
from app.models import Usuario, Repositorio

router = APIRouter(prefix="/repositories", tags=["Repositorios"])


@router.post("", response_model=RepositorioResponse, status_code=status.HTTP_201_CREATED)
def create_repositorio(
    repositorio_in: RepositorioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    repo_service = RepositoryService(db)
    repositorio = repo_service.create_repositorio(repositorio_in, current_user.id)
    return repositorio


@router.get("", response_model=List[RepositorioWithStats])
def list_repositorios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    repo_service = RepositoryService(db)
    if current_user.rol == "administrador":
        repositorios = repo_service.get_all_repositorios(skip, limit)
    else:
        repositorios = repo_service.get_repositorios_by_user(current_user.id, skip, limit)
    doc_service = DocumentService(db)
    return [
        RepositorioWithStats(
            **repositorio.__dict__,
            total_documentos=(stats := doc_service.get_documentos_stats(repositorio.id))["total"],
            documentos_por_estado=stats["por_estado"],
            documentos_por_categoria=stats["por_categoria"],
        )
        for repositorio in repositorios
    ]


@router.get("/{repositorio_id}", response_model=RepositorioWithStats)
def get_repositorio(
    repositorio_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    repo_service = RepositoryService(db)
    doc_service = DocumentService(db)
    
    repositorio = repo_service.get_repositorio(repositorio_id)
    if not repositorio:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")
    
    # Verificar permisos
    if current_user.rol != "administrador" and repositorio.usuario_creador_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene acceso a este repositorio")
    
    stats = doc_service.get_documentos_stats(repositorio_id)
    
    return RepositorioWithStats(
        **repositorio.__dict__,
        total_documentos=stats["total"],
        documentos_por_estado=stats["por_estado"],
        documentos_por_categoria=stats["por_categoria"],
    )


@router.put("/{repositorio_id}", response_model=RepositorioResponse)
def update_repositorio(
    repositorio_id: UUID,
    repositorio_in: RepositorioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    repo_service = RepositoryService(db)
    repositorio = repo_service.get_repositorio(repositorio_id)
    if not repositorio:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")
    
    if current_user.rol != "administrador" and repositorio.usuario_creador_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para modificar este repositorio")
    
    updated = repo_service.update_repositorio(repositorio_id, repositorio_in)
    return updated


@router.delete("/{repositorio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repositorio(
    repositorio_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    repo_service = RepositoryService(db)
    repositorio = repo_service.get_repositorio(repositorio_id)
    if not repositorio:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")
    
    if current_user.rol != "administrador" and repositorio.usuario_creador_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para eliminar este repositorio")
    
    if not repo_service.delete_repositorio(repositorio_id):
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")