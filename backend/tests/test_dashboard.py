from app.core.database import SessionLocal
from app.main import app
from app.models.analysis import ResumeAnalysis
from app.models.resume import Resume
from app.models.resume_version import ResumeVersion
from fastapi.testclient import TestClient

client = TestClient(app)


def test_dashboard_includes_resume_versions_and_match_metrics():
    db = SessionLocal()
    resume = Resume(filename="dashboard-test.txt", file_type="txt", raw_text="Python resume")
    db.add(resume)
    db.commit()
    db.refresh(resume)
    analysis = ResumeAnalysis(
        resume_id=resume.id,
        target_role="Backend Developer",
        candidate_name="Dashboard Test",
        match_score=80,
        missing_skills=[{"skill": "FastAPI"}],
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    analysis_id = analysis.id
    try:
        db.add(ResumeVersion(
            analysis_id=analysis_id,
            version_number=1,
            parsed_data={"personal_info": {"name": "Dashboard Test"}},
        ))
        db.commit()
        response = client.get("/api/v1/dashboard/summary")
        assert response.status_code == 200
        data = response.json()
        version = next(item for item in data["resume_versions"] if item["analysis_id"] == analysis_id)
        assert version["version_number"] == 1
        assert version["parsed_resume"]["personal_info"]["name"] == "Dashboard Test"
        assert data["metrics"]["average_match_score"] > 0
        assert all(item["count"] > 0 and item["skill"] for item in data["skill_gaps"])
    finally:
        db.query(ResumeVersion).filter_by(analysis_id=analysis_id).delete()
        db.query(ResumeAnalysis).filter_by(id=analysis_id).delete()
        db.query(Resume).filter_by(id=resume.id).delete()
        db.commit()
        db.close()