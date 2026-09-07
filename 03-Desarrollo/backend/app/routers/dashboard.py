from uuid import UUID
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.schemas.dashboard import DashboardStats, LogProcesamientoResumen
from app.services.document_service import DocumentService
from app.services.repository_service import RepositoryService
from app.models import Documento, LogProcesamiento, Usuario, Repositorio

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardStats)
def dashboard_summary(
    repositorio_id: UUID = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    doc_service = DocumentService(db)
    repo_service = RepositoryService(db)
    
    # Stats generales
    if current_user.rol == "administrador":
        total_repos = db.query(Repositorio).count()
        total_docs = db.query(Documento).count()
        total_usuarios = db.query(Usuario).count()
    else:
        total_repos = repo_service.count_repositorios_by_user(current_user.id)
        total_docs = doc_service.count_documentos_by_repositorio(repositorio_id) if repositorio_id else 0
        total_usuarios = 1
    
    # Stats de documentos (filtrar por repositorio si se especifica)
    doc_query = db.query(Documento)
    if repositorio_id:
        doc_query = doc_query.filter(Documento.repositorio_id == repositorio_id)
    elif current_user.rol != "administrador":
        repos = repo_service.get_repositorios_by_user(current_user.id)
        repo_ids = [r.id for r in repos]
        doc_query = doc_query.filter(Documento.repositorio_id.in_(repo_ids))
    
    por_categoria = dict(
        doc_query.with_entities(Documento.categoria, func.count(Documento.id))
        .filter(Documento.categoria.isnot(None))
        .group_by(Documento.categoria)
        .all()
    )
    
    por_estado = dict(
        doc_query.with_entities(Documento.estado, func.count(Documento.id))
        .group_by(Documento.estado)
        .all()
    )
    
    # Últimos errores
    logs_query = db.query(LogProcesamiento).join(Documento).filter(
        LogProcesamiento.tipo.like("error%")
    )
    if repositorio_id:
        logs_query = logs_query.filter(Documento.repositorio_id == repositorio_id)
    elif current_user.rol != "administrador":
        repos = repo_service.get_repositorios_by_user(current_user.id)
        repo_ids = [r.id for r in repos]
        logs_query = logs_query.filter(Documento.repositorio_id.in_(repo_ids))
    
    ultimos_errores = logs_query.order_by(LogProcesamiento.creado_en.desc()).limit(10).all()
    
    errores_resumen = [
        LogProcesamientoResumen(
            id=log.id,
            documento_id=log.documento_id,
            nombre_archivo=log.documento.nombre_archivo if log.documento else "Desconocido",
            tipo=log.tipo,
            mensaje=log.mensaje,
            creado_en=log.creado_en
        )
        for log in ultimos_errores
    ]
    
    return DashboardStats(
        total_repositorios=total_repos,
        total_documentos=total_docs,
        total_usuarios=total_usuarios,
        documentos_por_categoria=por_categoria,
        documentos_por_estado=por_estado,
        errores_recientes=errores_resumen
    )


@router.get("/logs", response_model=List[LogProcesamientoResumen])
def get_logs(
    repositorio_id: UUID = None,
    tipo: str = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    query = db.query(LogProcesamiento).join(Documento)
    
    if repositorio_id:
        query = query.filter(Documento.repositorio_id == repositorio_id)
    elif current_user.rol != "administrador":
        repo_service = RepositoryService(db)
        repos = repo_service.get_repositorios_by_user(current_user.id)
        repo_ids = [r.id for r in repos]
        query = query.filter(Documento.repositorio_id.in_(repo_ids))
    
    if tipo:
        query = query.filter(LogProcesamiento.tipo == tipo)
    
    logs = query.order_by(LogProcesamiento.creado_en.desc()).limit(limit).all()
    
    return [
        LogProcesamientoResumen(
            id=log.id,
            documento_id=log.documento_id,
            nombre_archivo=log.documento.nombre_archivo if log.documento else "Desconocido",
            tipo=log.tipo,
            mensaje=log.mensaje,
            creado_en=log.creado_en
        )
        for log in logs
    ]


@router.post("/documents/{documento_id}/reprocess")
def reprocesar_documento(
    documento_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    from app.services.processing_service import ProcessingService
    
    doc_service = DocumentService(db)
    documento = doc_service.get_documento(documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    # Resetear estado
    doc_service.update_documento(documento_id, {"estado": "pendiente", "categoria": None, "resumen": None, "campos_extraidos": None})
    
    # Eliminar vectores y fragmentos antiguos antes de volver a indexar
    from app.models import Fragmento
    old_fragments = db.query(Fragmento).filter(Fragmento.documento_id == documento_id).all()
    from app.services.vector_store import delete_document_vectors
    delete_document_vectors([fragment.vector_id for fragment in old_fragments])
    db.query(Fragmento).filter(Fragmento.documento_id == documento_id).delete()
    
    db.commit()
    
    # Procesar de forma síncrona para reutilizar el mismo pipeline de carga
    processing_service = ProcessingService(db)
    success = processing_service.process_document_with_ai(documento_id)
    
    return {"message": "Reprocesamiento completado", "exito": success}