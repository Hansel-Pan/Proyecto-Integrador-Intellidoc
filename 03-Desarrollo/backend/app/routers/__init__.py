from app.routers.auth import router as auth_router
from app.routers.repositories import router as repositories_router
from app.routers.documents import router as documents_router
from app.routers.chat import router as chat_router
from app.routers.dashboard import router as dashboard_router

__all__ = [
    "auth_router",
    "repositories_router",
    "documents_router",
    "chat_router",
    "dashboard_router",
]