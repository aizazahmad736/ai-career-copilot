from fastapi import APIRouter
from app.api.v1.endpoints import health, cv, jobs

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(cv.router, prefix="/cv", tags=["CV & Skill Gap Analysis"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Job Search & Matching"])
