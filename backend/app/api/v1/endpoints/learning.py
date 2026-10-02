from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.analysis import ResumeAnalysis
from app.models.learning_plan import LearningPlan
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.learning_plan import LearningPlanRequest, LearningPlanResponse, MilestoneProgressRequest
from app.services.learning_plan_service import build_learning_milestones

router = APIRouter()


@router.post("/plans", response_model=LearningPlanResponse)
def create_learning_plan(
    payload: LearningPlanRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    analysis = db.get(ResumeAnalysis, payload.analysis_id)
    if analysis is None or (user is not None and analysis.user_id != user.id):
        raise HTTPException(status_code=404, detail="Resume analysis not found")

    plan = db.query(LearningPlan).filter_by(analysis_id=analysis.id).first()
    milestones = build_learning_milestones(analysis, payload.duration_weeks)
    if plan is None:
        plan = LearningPlan(analysis_id=analysis.id)
        db.add(plan)
    plan.duration_weeks = payload.duration_weeks
    plan.milestones = milestones
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/plans/{analysis_id}", response_model=LearningPlanResponse)
def get_learning_plan(
    analysis_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    plan = db.query(LearningPlan).filter_by(analysis_id=analysis_id).first()
    analysis = db.get(ResumeAnalysis, analysis_id)
    if plan is None or analysis is None or (user is not None and analysis.user_id != user.id):
        raise HTTPException(status_code=404, detail="Learning plan not found")
    return plan


@router.patch("/plans/{plan_id}/milestones/{week_number}", response_model=LearningPlanResponse)
def update_milestone_progress(
    plan_id: int,
    week_number: int,
    payload: MilestoneProgressRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    plan = db.get(LearningPlan, plan_id)
    analysis = db.get(ResumeAnalysis, plan.analysis_id) if plan else None
    if plan is None or analysis is None or (user is not None and analysis.user_id != user.id):
        raise HTTPException(status_code=404, detail="Learning plan not found")
    if not any(item["week"] == week_number for item in plan.milestones):
        raise HTTPException(status_code=404, detail="Milestone not found")
    plan.milestones = [
        {**item, "completed": payload.completed} if item["week"] == week_number else item
        for item in plan.milestones
    ]
    db.commit()
    db.refresh(plan)
    return plan