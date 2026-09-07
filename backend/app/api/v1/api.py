from fastapi import APIRouter
from app.api.v1.endpoints import health, cv

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(cv.router, prefix="/cv", tags=["CV & Skill Gap Analysis"])
