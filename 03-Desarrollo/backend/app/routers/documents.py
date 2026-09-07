from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import os
from pathlib import Path
import aiofiles

from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_active_user, require_admin
from app.schemas.documento import DocumentoCreate, DocumentoUpdate, DocumentoResponse, DocumentoListResponse, DocumentoSearchResult
from app.services.document_service import DocumentService
from app.services.repository_service import RepositoryService
from app.services.processing_service import ProcessingService
from app.services.ai_service import AIService
from app.models import Usuario, Documento

router = APIRouter(prefix="/documents", tags=["Documentos"])

# Directorio de almacenamiento
STORAGE_DIR = Path(__file__).resolve().parents[2] / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def validate_file(file: UploadFile) -> None:
    """Validar tipo y tamaño de archivo."""
    ext = file.filename.split(".")[-1].lower() if file.filename else ""
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Tipo de archivo no permitido. Permitidos: {', '.join(settings.ALLOWED_EXTENSIONS)}")


@router.post("", response_model=DocumentoResponse, status_code=status.HTTP_201_CREATED)
async def upload_documento(
    repositorio_id: UUID = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    validate_file(file)
    
    repo_service = RepositoryService(db)
    repositorio = repo_service.get_repositorio(repositorio_id)
    if not repositorio:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")
    
    if current_user.rol != "administrador" and repositorio.usuario_creador_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene acceso a este repositorio")
    
    # Guardar archivo en disco
    file_ext = file.filename.rsplit(".", 1)[-1].lower()
    original_name = Path(file.filename or "documento").name
    safe_filename = f"{current_user.id}_{repositorio_id}_{original_name}"
    file_path = STORAGE_DIR / safe_filename
    
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read(settings.MAX_FILE_SIZE + 1)
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Archivo demasiado grande. Máximo {settings.MAX_FILE_SIZE / (1024 * 1024)} MB",
            )
        await f.write(content)
    
    # Crear registro en BD
    doc_service = DocumentService(db)
    documento_in = DocumentoCreate(
        repositorio_id=repositorio_id,
        nombre_archivo=file.filename,
        formato=file_ext,
        ruta_almacenamiento=str(file_path),
    )
    
    documento = doc_service.create_documento(documento_in, current_user.id)
    
    # Procesar documento SÍNCRONAMENTE (extracción + embeddings + IA)
    processing_service = ProcessingService(db)
    success = processing_service.process_document_with_ai(documento.id)
    
    # Recargar documento para devolver datos actualizados
    documento = doc_service.get_documento(documento.id)
    return documento


@router.get("", response_model=List[DocumentoListResponse])
def list_documentos(
    repositorio_id: Optional[UUID] = None,
    estado: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    doc_service = DocumentService(db)
    repo_service = RepositoryService(db)
    
    if repositorio_id:
        repositorio = repo_service.get_repositorio(repositorio_id)
        if not repositorio:
            raise HTTPException(status_code=404, detail="Repositorio no encontrado")
        if current_user.rol != "administrador" and repositorio.usuario_creador_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene acceso a este repositorio")
        documentos = doc_service.get_documentos_by_repositorio(repositorio_id, skip, limit, estado)
    else:
        # Listar todos los documentos accesibles
        if current_user.rol == "administrador":
            query = db.query(Documento)
        else:
            # Obtener repositorios del usuario
            repos = repo_service.get_repositorios_by_user(current_user.id)
            repo_ids = [r.id for r in repos]
            query = db.query(Documento).filter(Documento.repositorio_id.in_(repo_ids))
        
        if estado:
            query = query.filter(Documento.estado == estado)
        documentos = query.order_by(Documento.creado_en.desc()).offset(skip).limit(limit).all()
    
    return documentos


@router.get("/search", response_model=List[DocumentoSearchResult])
def search_documentos(
    q: str,
    repositorio_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    doc_service = DocumentService(db)
    repo_service = RepositoryService(db)
    
    if repositorio_id:
        repositorio = repo_service.get_repositorio(repositorio_id)
        if not repositorio:
            raise HTTPException(status_code=404, detail="Repositorio no encontrado")
        if current_user.rol != "administrador" and repositorio.usuario_creador_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene acceso a este repositorio")
    else:
        repositorio = None
    
    resultados = doc_service.search_documentos(q, repositorio_id, skip, limit)
    
    # Enriquecer con nombre de repositorio
    resultados_con_repo = []
    for doc in resultados:
        repo = repo_service.get_repositorio(doc.repositorio_id)
        resultados_con_repo.append(DocumentoSearchResult(
            **doc.__dict__,
            repositorio_nombre=repo.nombre if repo else "Desconocido",
            coincidencias=[q]  # Simplificado
        ))
    
    return resultados_con_repo


@router.get("/{documento_id}", response_model=DocumentoResponse)
def get_documento(
    documento_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    doc_service = DocumentService(db)
    documento = doc_service.get_documento(documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    repo_service = RepositoryService(db)
    repositorio = repo_service.get_repositorio(documento.repositorio_id)
    if current_user.rol != "administrador" and repositorio.usuario_creador_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene acceso a este documento")
    
    return documento


@router.get("/{documento_id}/download")
def download_documento(
    documento_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    from fastapi.responses import FileResponse
    doc_service = DocumentService(db)
    documento = doc_service.get_documento(documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    repo_service = RepositoryService(db)
    repositorio = repo_service.get_repositorio(documento.repositorio_id)
    if current_user.rol != "administrador" and repositorio.usuario_creador_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene acceso a este documento")
    
    if not os.path.exists(documento.ruta_almacenamiento):
        raise HTTPException(status_code=404, detail="Archivo no encontrado en almacenamiento")
    
    return FileResponse(
        documento.ruta_almacenamiento,
        filename=documento.nombre_archivo,
        media_type="application/octet-stream",
    )


@router.put("/{documento_id}", response_model=DocumentoResponse)
def update_documento(
    documento_id: UUID,
    documento_in: DocumentoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    doc_service = DocumentService(db)
    documento = doc_service.get_documento(documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    repo_service = RepositoryService(db)
    repositorio = repo_service.get_repositorio(documento.repositorio_id)
    if current_user.rol != "administrador" and repositorio.usuario_creador_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para modificar este documento")
    
    updated = doc_service.update_documento(documento_id, documento_in)
    return updated


@router.delete("/{documento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_documento(
    documento_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    doc_service = DocumentService(db)
    documento = doc_service.get_documento(documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    repo_service = RepositoryService(db)
    repositorio = repo_service.get_repositorio(documento.repositorio_id)
    if current_user.rol != "administrador" and repositorio.usuario_creador_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para eliminar este documento")
    
    # Eliminar archivo físico
    if os.path.exists(documento.ruta_almacenamiento):
        os.remove(documento.ruta_almacenamiento)
    
    if not doc_service.delete_documento(documento_id):
        raise HTTPException(status_code=404, detail="Documento no encontrado")