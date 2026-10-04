from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.analysis import ResumeAnalysis
from app.models.job import JobSearch
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.job import JobSearchRequest, JobSearchResponse
from app.services.job_search_service import job_search_service
from app.services.job_matching_service import job_matching_service

router = APIRouter()

@router.get("/sources")
def get_job_sources():
    return {
        "sources": [
            {"name": "Remotive", "type": "job_api", "requires_key": False, "configured": True},
            {"name": "Arbeitnow", "type": "job_api", "requires_key": False, "configured": True},
            {"name": "Tavily", "type": "web_search", "requires_key": True, "configured": bool(settings.TAVILY_API_KEY)},
            {"name": "Serper", "type": "web_search", "requires_key": True, "configured": bool(settings.SERPER_API_KEY)},
        ]
    }

@router.post("/search", response_model=JobSearchResponse)
def search_jobs(
    payload: JobSearchRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    analysis_id = payload.analysis_id
    if analysis_id is not None:
        analysis = db.get(ResumeAnalysis, analysis_id)
        if analysis is None or (user is not None and analysis.user_id != user.id):
            raise HTTPException(status_code=404, detail="Resume analysis not found")

    # 1. Collect listings from every configured provider
    raw_jobs, sources_used, source_errors, query, is_demo_mode = job_search_service.search(
        target_role=payload.target_role,
        experience_level=payload.experience_level,
        location=payload.location,
        tavily_api_key=payload.tavily_api_key,
        serper_api_key=payload.serper_api_key,
        skills=payload.skills,
    )

    # 2. Score and rank against the candidate's skills
    matches, total_found = job_matching_service.rank_jobs(
        jobs=raw_jobs,
        skills=payload.skills,
        target_role=payload.target_role,
        experience_level=payload.experience_level,
        location=payload.location,
        remote_only=payload.remote_only,
        limit=payload.limit,
    )

    # 3. Persist the search run (only link an analysis that actually exists)
    search_record = JobSearch(
        user_id=user.id if user else None,
        analysis_id=analysis_id,
        target_role=payload.target_role,
        experience_level=payload.experience_level,
        query=query,
        location=payload.location,
        remote_only=payload.remote_only,
        result_count=total_found,
        top_match_score=matches[0].match_score if matches else 0.0,
        sources_used=sources_used,
        results=[m.model_dump() for m in matches],
        is_demo_mode=is_demo_mode,
    )
    db.add(search_record)
    db.commit()
    db.refresh(search_record)

    return JobSearchResponse(
        id=search_record.id,
        target_role=payload.target_role,
        experience_level=payload.experience_level,
        query=query,
        total_found=total_found,
        sources_used=sources_used,
        source_errors=source_errors,
        is_demo_mode=is_demo_mode,
        jobs=matches,
    )
