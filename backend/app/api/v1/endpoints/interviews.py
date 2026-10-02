from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db, utcnow
from app.models.analysis import ResumeAnalysis
from app.models.interview import InterviewSession
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.interview import InterviewAnswerRequest, InterviewCreateRequest, InterviewSessionResponse
from app.services.interview_service import interview_service

router = APIRouter()


def _candidate_skills(analysis: ResumeAnalysis):
    return [skill for values in (analysis.extracted_skills or {}).values() if isinstance(values, list) for skill in values]


@router.post("/sessions", response_model=InterviewSessionResponse)
def create_interview(
    payload: InterviewCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if payload.mode not in {"mixed", "technical", "behavioral"}:
        raise HTTPException(status_code=422, detail="Mode must be mixed, technical, or behavioral")
    analysis = db.get(ResumeAnalysis, payload.analysis_id)
    if analysis is None or (user is not None and analysis.user_id != user.id):
        raise HTTPException(status_code=404, detail="Resume analysis not found")
    questions = interview_service.generate_questions(
        analysis.target_role, _candidate_skills(analysis), payload.mode, payload.question_count, payload.custom_gemini_api_key
    )
    session = InterviewSession(
        analysis_id=analysis.id,
        target_role=analysis.target_role,
        mode=payload.mode,
        questions=questions,
        responses=[],
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions/{session_id}", response_model=InterviewSessionResponse)
def get_interview(session_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.get(InterviewSession, session_id)
    if session is None or (user is not None and not _owns_analysis(db, session.analysis_id, user.id)):
        raise HTTPException(status_code=404, detail="Interview session not found")
    return session


@router.post("/sessions/{session_id}/answers", response_model=InterviewSessionResponse)
def answer_interview_question(
    session_id: int,
    payload: InterviewAnswerRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    session = db.get(InterviewSession, session_id)
    if session is None or (user is not None and not _owns_analysis(db, session.analysis_id, user.id)):
        raise HTTPException(status_code=404, detail="Interview session not found")
    if session.status == "completed":
        raise HTTPException(status_code=409, detail="Interview session is already complete")
    question_index = len(session.responses)
    if question_index >= len(session.questions):
        raise HTTPException(status_code=409, detail="No unanswered questions remain")
    analysis = db.get(ResumeAnalysis, session.analysis_id)
    skills = _candidate_skills(analysis) if analysis else []
    feedback = interview_service.evaluate_answer(
        session.questions[question_index]["question"], payload.answer, session.target_role, skills, payload.custom_gemini_api_key
    )
    session.responses = [
        *session.responses,
        {"question_index": question_index, "answer": payload.answer, **feedback},
    ]
    session.total_score = round(sum(item["overall_score"] for item in session.responses) / len(session.responses), 1)
    if len(session.responses) == len(session.questions):
        session.status = "completed"
        session.completed_at = datetime.now().replace(tzinfo=None)
    db.commit()
    db.refresh(session)
    return session


def _owns_analysis(db: Session, analysis_id: int, user_id: int) -> bool:
    analysis = db.get(ResumeAnalysis, analysis_id)
    return analysis is not None and analysis.user_id == user_id