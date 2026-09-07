from functools import lru_cache
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings


@lru_cache(maxsize=1)
def get_chroma_client() -> Any:
    """Return one persistent Chroma client shared by indexing and search."""
    configured_path = Path(settings.CHROMADB_PATH)
    if not configured_path.is_absolute():
        configured_path = Path(__file__).resolve().parents[2] / configured_path
    configured_path.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(configured_path),
        settings=ChromaSettings(anonymized_telemetry=False),
    )


@lru_cache(maxsize=1)
def get_document_collection() -> Any:
    return get_chroma_client().get_or_create_collection(
        name="documentos",
        metadata={"hnsw:space": "cosine"},
    )


def delete_document_vectors(vector_ids: list[str]) -> None:
    if vector_ids:
        get_document_collection().delete(ids=vector_ids)
