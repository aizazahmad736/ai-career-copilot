from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "2.0.0 (Phase 2)",
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "web_search_configured": bool(settings.TAVILY_API_KEY or settings.SERPER_API_KEY),
    }
