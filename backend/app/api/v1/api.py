from fastapi import APIRouter
from app.api.v1.endpoints import health, cv, jobs, learning, interviews, dashboard, auth, applications

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(cv.router, prefix="/cv", tags=["CV & Skill Gap Analysis"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Job Search & Matching"])
api_router.include_router(learning.router, prefix="/learning", tags=["Learning Plans"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["Mock Interviews"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Career Dashboard"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(applications.router, prefix="/applications", tags=["Application Tracking"])
