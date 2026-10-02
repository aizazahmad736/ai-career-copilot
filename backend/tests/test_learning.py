from app.core.database import SessionLocal
from app.main import app
from app.models.analysis import ResumeAnalysis
from app.models.learning_plan import LearningPlan
from fastapi.testclient import TestClient

client = TestClient(app)


def test_learning_plan_generates_and_persists_progress():
    db = SessionLocal()
    analysis = ResumeAnalysis(
        target_role="Frontend Developer",
        recommendations=[{"target_skill": "React", "learning_path": ["Build a component", "Add tests"]}],
        missing_skills=[{"skill": "React"}],
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    analysis_id = analysis.id
    plan_id = None
    try:
        response = client.post("/api/v1/learning/plans", json={"analysis_id": analysis_id, "duration_weeks": 4})
        assert response.status_code == 200
        plan = response.json()
        plan_id = plan["id"]
        assert len(plan["milestones"]) == 4
        assert plan["milestones"][0]["skills"] == ["React"]
        assert plan["milestones"][0]["resources"][0]["url"] == "https://react.dev/learn"

        progress = client.patch(f"/api/v1/learning/plans/{plan_id}/milestones/1", json={"completed": True})
        assert progress.status_code == 200
        assert progress.json()["milestones"][0]["completed"] is True
        assert client.get(f"/api/v1/learning/plans/{analysis_id}").status_code == 200
    finally:
        if plan_id is not None:
            db.query(LearningPlan).filter_by(id=plan_id).delete()
        db.query(ResumeAnalysis).filter_by(id=analysis_id).delete()
        db.commit()
        db.close()