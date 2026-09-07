import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from sentence_transformers import SentenceTransformer
from sqlalchemy import or_

from app.core.config import settings
from app.models import Documento, Fragmento, ConsultaChat, Repositorio
from app.services.ai_service import AIService
from app.services.vector_store import get_document_collection


class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
        self.embedding_model = None

    def _get_embedding_model(self) -> SentenceTransformer:
        if self.embedding_model is None:
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        return self.embedding_model

    def _get_chroma_collection(self):
        return get_document_collection()

    def search_semantic(
        self,
        query: str,
        usuario_id: uuid.UUID,
        repositorio_id: Optional[uuid.UUID] = None,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Búsqueda semántica usando embeddings y ChromaDB."""
        accessible_repos = self.db.query(Repositorio.id)
        if repositorio_id:
            accessible_repos = accessible_repos.filter(Repositorio.id == repositorio_id)
        else:
            accessible_repos = self.db.query(Repositorio.id).filter(
                Repositorio.usuario_creador_id == usuario_id
            )
        repo_ids = [row[0] for row in accessible_repos.all()]
        if not repo_ids:
            return []

        doc_ids = [
            str(row[0])
            for row in self.db.query(Documento.id)
            .filter(Documento.repositorio_id.in_(repo_ids), Documento.estado == "procesado")
            .all()
        ]
        if not doc_ids:
            return []

        collection = self._get_chroma_collection()
        if collection.count() == 0:
            return self._search_fragments_fallback(query, doc_ids, top_k)
        
        # Generar embedding de la pregunta
        model = self._get_embedding_model()
        query_embedding = model.encode([query], convert_to_tensor=False).tolist()[0]
        
        # Buscar en ChromaDB
        where_filter = {"documento_id": {"$in": doc_ids}}
        
        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, collection.count()),
                where=where_filter,
                include=["documents", "metadatas", "distances"],
            )
        except Exception:
            return self._search_fragments_fallback(query, doc_ids, top_k)
        
        # Formatear resultados
        fragmentos = []
        if results["ids"] and results["ids"][0]:
            for i, (doc_id, document, metadata, distance) in enumerate(zip(
                results["ids"][0], results["documents"][0], results["metadatas"][0], results["distances"][0]
            )):
                # Obtener info del documento
                doc = self.db.query(Documento).filter(Documento.id == uuid.UUID(metadata["documento_id"])).first()
                if doc:
                    similitud = 1 - distance  # Convertir distancia coseno a similitud
                    fragmentos.append({
                        "documento_id": metadata["documento_id"],
                        "nombre_archivo": doc.nombre_archivo,
                        "texto": document,
                        "similitud": similitud,
                        "orden": metadata.get("orden", 0)
                    })
        
        return fragmentos

    def _search_fragments_fallback(
        self, query: str, doc_ids: List[str], top_k: int
    ) -> List[Dict[str, Any]]:
        """Use stored text when the vector store is empty or unavailable."""
        terms = [term.lower() for term in query.split() if len(term) > 2]
        fragments = self.db.query(Fragmento).filter(
            Fragmento.documento_id.in_([uuid.UUID(doc_id) for doc_id in doc_ids]),
            or_(*[Fragmento.texto.ilike(f"%{term}%") for term in terms]) if terms else True,
        ).all()
        ranked = sorted(
            fragments,
            key=lambda fragment: sum(
                fragment.texto.lower().count(term) for term in terms
            ),
            reverse=True,
        )[:top_k]
        return [
            {
                "documento_id": str(fragment.documento_id),
                "nombre_archivo": self.db.query(Documento.nombre_archivo)
                .filter(Documento.id == fragment.documento_id).scalar(),
                "texto": fragment.texto,
                "similitud": 0.5,
                "orden": fragment.orden,
            }
            for fragment in ranked
        ]

    def chat(self, pregunta: str, usuario_id: uuid.UUID, repositorio_id: Optional[uuid.UUID] = None) -> Dict[str, Any]:
        """Procesar pregunta RAG completa."""
        # 1. Búsqueda semántica
        fragmentos = self.search_semantic(pregunta, usuario_id, repositorio_id, top_k=5)
        
        # 2. Generar respuesta con LLM
        respuesta = self.ai_service.responder_pregunta(pregunta, fragmentos)
        
        # 3. Preparar fuentes para guardar
        fuentes = []
        for frag in fragmentos:
            fuentes.append({
                "documento_id": frag["documento_id"],
                "nombre_archivo": frag["nombre_archivo"],
                "similitud": frag["similitud"]
            })
        
        # 4. Guardar consulta en BD
        consulta = ConsultaChat(
            usuario_id=usuario_id,
            pregunta=pregunta,
            respuesta=respuesta,
            documentos_fuente=fuentes
        )
        self.db.add(consulta)
        self.db.commit()
        self.db.refresh(consulta)
        
        return {
            "respuesta": respuesta,
            "fuentes": [
                {
                    "documento_id": f["documento_id"],
                    "nombre_archivo": f["nombre_archivo"],
                    "fragmento_texto": next((fr["texto"] for fr in fragmentos if fr["documento_id"] == f["documento_id"]), ""),
                    "similitud": f["similitud"]
                }
                for f in fuentes
            ],
            "consulta_id": str(consulta.id)
        }

    def get_chat_history(self, usuario_id: uuid.UUID, limit: int = 20) -> List[ConsultaChat]:
        return self.db.query(ConsultaChat).filter(
            ConsultaChat.usuario_id == usuario_id
        ).order_by(ConsultaChat.creado_en.desc()).limit(limit).all()