from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.core.database import get_db
from app.models.analysis import ResumeAnalysis
from app.models.application import Application
from app.models.user import User
from app.schemas.application import ApplicationCreateRequest, ApplicationResponse, ApplicationStatusRequest

router = APIRouter()


def _application_query(db: Session, user: Optional[User]):
    query = db.query(Application)
    if user is None:
        return query.filter(Application.user_id.is_(None))
    return query.filter(Application.user_id == user.id)


@router.get("", response_model=list[ApplicationResponse])
def list_applications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return _application_query(db, user).order_by(Application.updated_at.desc()).all()


@router.post("", response_model=ApplicationResponse)
def save_application(
    payload: ApplicationCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if payload.analysis_id is not None:
        analysis = db.get(ResumeAnalysis, payload.analysis_id)
        if analysis is None or (user is not None and analysis.user_id != user.id):
            raise HTTPException(status_code=404, detail="Resume analysis not found")
    existing = _application_query(db, user).filter_by(job_key=payload.job_key).first()
    if existing:
        return existing
    application = Application(
        user_id=user.id if user else None,
        analysis_id=payload.analysis_id,
        job_key=payload.job_key,
        target_role=payload.target_role,
        title=payload.title,
        company=payload.company,
        url=payload.url,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    payload: ApplicationStatusRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    application = _application_query(db, user).filter_by(id=application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    application.status = payload.status
    if "notes" in payload.model_fields_set:
        application.notes = payload.notes
    db.commit()
    db.refresh(application)
    return application