from uuid import UUID
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Documento, Repositorio, Fragmento, LogProcesamiento
from app.schemas.documento import DocumentoCreate, DocumentoUpdate


class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def create_documento(self, documento_in: DocumentoCreate, usuario_carga_id: UUID) -> Documento:
        repositorio = self.db.query(Repositorio).filter(Repositorio.id == documento_in.repositorio_id).first()
        if not repositorio:
            raise ValueError("Repositorio no encontrado")
        
        documento = Documento(
            repositorio_id=documento_in.repositorio_id,
            usuario_carga_id=usuario_carga_id,
            nombre_archivo=documento_in.nombre_archivo,
            formato=documento_in.formato,
            ruta_almacenamiento=documento_in.ruta_almacenamiento,
            estado="pendiente",
        )
        self.db.add(documento)
        self.db.commit()
        self.db.refresh(documento)
        return documento

    def get_documento(self, documento_id: UUID) -> Optional[Documento]:
        return self.db.query(Documento).filter(Documento.id == documento_id).first()

    def get_documentos_by_repositorio(
        self, 
        repositorio_id: UUID, 
        skip: int = 0, 
        limit: int = 100,
        estado: Optional[str] = None,
    ) -> List[Documento]:
        query = self.db.query(Documento).filter(Documento.repositorio_id == repositorio_id)
        if estado:
            query = query.filter(Documento.estado == estado)
        return query.order_by(Documento.creado_en.desc()).offset(skip).limit(limit).all()

    def count_documentos_by_repositorio(self, repositorio_id: UUID) -> int:
        return self.db.query(Documento).filter(Documento.repositorio_id == repositorio_id).count()

    def update_documento(self, documento_id: UUID, documento_in: DocumentoUpdate) -> Optional[Documento]:
        documento = self.get_documento(documento_id)
        if not documento:
            return None
        
        update_data = (
            documento_in.model_dump(exclude_unset=True)
            if hasattr(documento_in, "model_dump")
            else documento_in
        )
        for field, value in update_data.items():
            setattr(documento, field, value)
        
        self.db.commit()
        self.db.refresh(documento)
        return documento

    def delete_documento(self, documento_id: UUID) -> bool:
        documento = self.get_documento(documento_id)
        if not documento:
            return False
        self.db.delete(documento)
        self.db.commit()
        return True

    def add_fragmento(self, documento_id: UUID, texto: str, vector_id: str, orden: int) -> Fragmento:
        fragmento = Fragmento(
            documento_id=documento_id,
            texto=texto,
            vector_id=vector_id,
            orden=orden,
        )
        self.db.add(fragmento)
        self.db.commit()
        self.db.refresh(fragmento)
        return fragmento

    def get_fragmentos_by_documento(self, documento_id: UUID) -> List[Fragmento]:
        return self.db.query(Fragmento).filter(Fragmento.documento_id == documento_id).order_by(Fragmento.orden).all()

    def log_procesamiento(self, documento_id: UUID, tipo: str, mensaje: str) -> LogProcesamiento:
        log = LogProcesamiento(
            documento_id=documento_id,
            tipo=tipo,
            mensaje=mensaje,
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_logs_by_documento(self, documento_id: UUID) -> List[LogProcesamiento]:
        return self.db.query(LogProcesamiento).filter(LogProcesamiento.documento_id == documento_id).order_by(LogProcesamiento.creado_en.desc()).all()

    def get_documentos_stats(self, repositorio_id: Optional[UUID] = None) -> Dict[str, Any]:
        query = self.db.query(Documento)
        if repositorio_id:
            query = query.filter(Documento.repositorio_id == repositorio_id)
        
        total = query.count()
        
        por_categoria = dict(
            query.with_entities(Documento.categoria, func.count(Documento.id))
            .filter(Documento.categoria.isnot(None))
            .group_by(Documento.categoria)
            .all()
        )
        
        por_estado = dict(
            query.with_entities(Documento.estado, func.count(Documento.id))
            .group_by(Documento.estado)
            .all()
        )
        
        return {
            "total": total,
            "por_categoria": por_categoria,
            "por_estado": por_estado,
        }

    def search_documentos(
        self, 
        query_text: str, 
        repositorio_id: Optional[UUID] = None,
        skip: int = 0, 
        limit: int = 20
    ) -> List[Documento]:
        query = self.db.query(Documento).filter(
            Documento.estado == "procesado",
            Documento.resumen.ilike(f"%{query_text}%") | 
            Documento.nombre_archivo.ilike(f"%{query_text}%") |
            Documento.campos_extraidos.cast(str).ilike(f"%{query_text}%")
        )
        if repositorio_id:
            query = query.filter(Documento.repositorio_id == repositorio_id)
        return query.order_by(Documento.creado_en.desc()).offset(skip).limit(limit).all()