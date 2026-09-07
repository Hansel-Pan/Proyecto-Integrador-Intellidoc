from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.schemas.chat import ChatRequest, ChatResponse, FuenteDocumento, ConsultaChatInDB
from app.services.search_service import SearchService
from app.models import Usuario

router = APIRouter(prefix="/chat", tags=["Chat RAG"])


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    search_service = SearchService(db)
    resultado = search_service.chat(request.pregunta, current_user.id, request.repositorio_id)
    
    fuentes = [
        FuenteDocumento(
            documento_id=UUID(f["documento_id"]),
            nombre_archivo=f["nombre_archivo"],
            fragmento_texto=f["fragmento_texto"],
            similitud=f["similitud"]
        )
        for f in resultado["fuentes"]
    ]
    
    return ChatResponse(respuesta=resultado["respuesta"], fuentes=fuentes)


@router.get("/history", response_model=List[ConsultaChatInDB])
def chat_history(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    search_service = SearchService(db)
    consultas = search_service.get_chat_history(current_user.id, limit)
    return consultas