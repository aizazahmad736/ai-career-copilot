from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.database import SessionLocal
from app.main import app
from app.models.analysis import ResumeAnalysis
from app.models.learning_plan import LearningPlan
from app.models.user import User
from app.services.auth_service import create_access_token, hash_password

client = TestClient(app)


def test_dashboard_and_learning_plans_are_account_scoped(monkeypatch):
    monkeypatch.setattr(settings, "AUTH_REQUIRED", True)
    db = SessionLocal()
    suffix = uuid4().hex
    first = User(email=f"owner-{suffix}@example.com", password_hash=hash_password("long-password-owner"))
    second = User(email=f"other-{suffix}@example.com", password_hash=hash_password("long-password-other"))
    db.add_all([first, second])
    db.commit()
    db.refresh(first)
    db.refresh(second)
    own_analysis = ResumeAnalysis(user_id=first.id, target_role="Frontend Developer", match_score=72)
    other_analysis = ResumeAnalysis(user_id=second.id, target_role="Backend Developer", match_score=95)
    db.add_all([own_analysis, other_analysis])
    db.commit()
    db.refresh(own_analysis)
    db.refresh(other_analysis)
    own_id = own_analysis.id
    other_id = other_analysis.id
    first_id = first.id
    second_id = second.id
    token = create_access_token(first_id, first.email)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        assert client.get("/api/v1/dashboard/summary").status_code == 401
        dashboard = client.get("/api/v1/dashboard/summary", headers=headers)
        assert dashboard.status_code == 200
        visible_ids = [item["analysis_id"] for item in dashboard.json()["resume_versions"]]
        assert own_id in visible_ids
        assert other_id not in visible_ids
        assert client.get(f"/api/v1/learning/plans/{other_id}", headers=headers).status_code == 404
        assert client.post(
            "/api/v1/learning/plans",
            headers=headers,
            json={"analysis_id": other_id},
        ).status_code == 404
    finally:
        db.query(LearningPlan).filter(LearningPlan.analysis_id.in_([own_id, other_id])).delete(synchronize_session=False)
        db.query(ResumeAnalysis).filter(ResumeAnalysis.id.in_([own_id, other_id])).delete(synchronize_session=False)
        db.query(User).filter(User.id.in_([first_id, second_id])).delete(synchronize_session=False)
        db.commit()
        db.close()
        monkeypatch.setattr(settings, "AUTH_REQUIRED", False)