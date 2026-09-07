from app.schemas.usuario import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioInDB,
    UsuarioResponse,
    Token,
    TokenData,
)
from app.schemas.repositorio import (
    RepositorioBase,
    RepositorioCreate,
    RepositorioUpdate,
    RepositorioInDB,
    RepositorioResponse,
    RepositorioWithStats,
)
from app.schemas.documento import (
    DocumentoBase,
    DocumentoCreate,
    DocumentoUpdate,
    DocumentoInDB,
    DocumentoResponse,
    DocumentoListResponse,
    DocumentoSearchResult,
)
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    FuenteDocumento,
    ConsultaChatInDB,
)
from app.schemas.dashboard import (
    DashboardSummary,
    DashboardStats,
    LogProcesamientoResumen,
)

__all__ = [
    # Usuario
    "UsuarioBase",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioInDB",
    "UsuarioResponse",
    "Token",
    "TokenData",
    # Repositorio
    "RepositorioBase",
    "RepositorioCreate",
    "RepositorioUpdate",
    "RepositorioInDB",
    "RepositorioResponse",
    "RepositorioWithStats",
    # Documento
    "DocumentoBase",
    "DocumentoCreate",
    "DocumentoUpdate",
    "DocumentoInDB",
    "DocumentoResponse",
    "DocumentoListResponse",
    "DocumentoSearchResult",
    # Chat
    "ChatRequest",
    "ChatResponse",
    "FuenteDocumento",
    "ConsultaChatInDB",
    # Dashboard
    "DashboardSummary",
    "DashboardStats",
    "LogProcesamientoResumen",
]