from backend.app.routers.analyze import router as analyze_router
from backend.app.routers.history import router as history_router
from backend.app.routers.health import router as health_router

__all__ = ["analyze_router", "history_router", "health_router"]
