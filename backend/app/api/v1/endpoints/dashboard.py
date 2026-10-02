from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.analysis import ResumeAnalysis
from app.models.application import Application
from app.models.interview import InterviewSession
from app.models.job import JobSearch
from app.models.learning_plan import LearningPlan
from app.models.resume import Resume
from app.models.resume_version import ResumeVersion
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = (
        db.query(ResumeAnalysis, Resume, ResumeVersion)
        .outerjoin(Resume, ResumeAnalysis.resume_id == Resume.id)
        .outerjoin(ResumeVersion, ResumeVersion.analysis_id == ResumeAnalysis.id)
    )
    if user is not None:
        query = query.filter(ResumeAnalysis.user_id == user.id)
    rows = query.order_by(ResumeAnalysis.created_at.asc(), ResumeAnalysis.id.asc()).all()
    filename_versions = Counter()
    versions = []
    analysis_ids = []
    for analysis, resume, snapshot in rows:
        analysis_ids.append(analysis.id)
        filename = resume.filename if resume else "Unknown resume"
        filename_versions[filename] += 1
        versions.append({
            "analysis_id": analysis.id,
            "resume_id": resume.id if resume else None,
            "filename": filename,
            "version_number": snapshot.version_number if snapshot else filename_versions[filename],
            "candidate_name": analysis.candidate_name,
            "target_role": analysis.target_role,
            "experience_level": analysis.experience_level,
            "headline": analysis.headline,
            "summary": analysis.summary,
            "match_score": analysis.match_score or 0,
            "ats_score": (analysis.ats_feedback or {}).get("overall_ats_score", 0),
            "matched_skills": analysis.matched_skills or [],
            "partial_skills": analysis.partial_skills or [],
            "missing_critical_skills": analysis.missing_skills or [],
            "bonus_skills": analysis.bonus_skills or [],
            "recommendations": analysis.recommendations or [],
            "ats_feedback": analysis.ats_feedback or {},
            "created_at": analysis.created_at,
            "parsed_resume": snapshot.parsed_data if snapshot else None,
        })

    plans = db.query(LearningPlan).filter(LearningPlan.analysis_id.in_(analysis_ids)).all() if analysis_ids else []
    sessions = (
        db.query(InterviewSession)
        .filter(InterviewSession.analysis_id.in_(analysis_ids))
        .order_by(InterviewSession.created_at.desc())
        .all()
        if analysis_ids else []
    )
    job_searches = (
        db.query(JobSearch)
        .filter(JobSearch.analysis_id.in_(analysis_ids))
        .order_by(JobSearch.created_at.desc())
        .all()
        if analysis_ids else []
    )
    applications_query = db.query(Application)
    if user is not None:
        applications_query = applications_query.filter(Application.user_id == user.id)
    else:
        applications_query = applications_query.filter(Application.user_id.is_(None))
    applications = applications_query.order_by(Application.updated_at.desc()).limit(20).all()
    completed_milestones = sum(
        1 for plan in plans for milestone in plan.milestones if milestone.get("completed")
    )
    total_milestones = sum(len(plan.milestones) for plan in plans)
    completed_interviews = [session for session in sessions if session.status == "completed"]
    missing_skills = Counter(
        item.get("skill")
        for analysis, _, _ in rows
        for item in (analysis.missing_skills or [])
        if item.get("skill")
    )
    scores = [analysis.match_score or 0 for analysis, _, _ in rows]

    return {
        "metrics": {
            "resume_versions": len(versions),
            "average_match_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "completed_learning_weeks": completed_milestones,
            "total_learning_weeks": total_milestones,
            "completed_interviews": len(completed_interviews),
            "average_interview_score": round(
                sum(session.total_score or 0 for session in completed_interviews) / len(completed_interviews), 1
            ) if completed_interviews else 0,
            "job_searches": len(job_searches),
            "tracked_applications": applications_query.count(),
        },
        "resume_versions": list(reversed(versions[-30:])),
        "match_trend": [
            {"date": analysis.created_at, "target_role": analysis.target_role, "score": analysis.match_score or 0}
            for analysis, _, _ in rows[-20:]
        ],
        "skill_gaps": [{"skill": skill, "count": count} for skill, count in missing_skills.most_common(8)],
        "interview_history": [
            {
                "id": session.id,
                "target_role": session.target_role,
                "mode": session.mode,
                "status": session.status,
                "score": session.total_score,
                "created_at": session.created_at,
            }
            for session in sessions[:10]
        ],
        "job_search_history": [
            {
                "id": search.id,
                "query": search.query,
                "target_role": search.target_role,
                "results": search.result_count,
                "top_match_score": search.top_match_score,
                "created_at": search.created_at,
            }
            for search in job_searches[:10]
        ],
        "applications": [
            {
                "id": application.id,
                "title": application.title,
                "company": application.company,
                "target_role": application.target_role,
                "status": application.status,
                "url": application.url,
                "updated_at": application.updated_at,
            }
            for application in applications
        ],
    }