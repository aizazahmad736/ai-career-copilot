from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine, migrate_account_columns
from app.api.v1.api import api_router

if settings.AUTH_REQUIRED:
    if settings.AUTH_SECRET == "local-development-only-change-me" or len(settings.AUTH_SECRET) < 32:
        raise RuntimeError("Set a unique AUTH_SECRET of at least 32 characters before requiring authentication.")
    if "*" in settings.CORS_ORIGINS:
        raise RuntimeError("Wildcard CORS origins are not allowed when authentication is required.")

# Initialize database schema tables
Base.metadata.create_all(bind=engine)
migrate_account_columns()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    description="AI Career Copilot API - An intelligent platform guiding students from CV to Skills to Jobs and Mock Interviews."
)

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API (Phase 2)",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
