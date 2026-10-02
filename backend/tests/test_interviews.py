from app.core.database import SessionLocal
from app.main import app
from app.models.analysis import ResumeAnalysis
from app.models.interview import InterviewSession
from fastapi.testclient import TestClient

client = TestClient(app)


def test_interview_session_scores_answers_and_completes():
    db = SessionLocal()
    analysis = ResumeAnalysis(
        target_role="Frontend Developer",
        extracted_skills={"frameworks": ["React", "JavaScript"]},
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    analysis_id = analysis.id
    session_id = None
    try:
        response = client.post("/api/v1/interviews/sessions", json={
            "analysis_id": analysis_id,
            "mode": "technical",
            "question_count": 3,
        })
        assert response.status_code == 200
        session_id = response.json()["id"]
        assert len(response.json()["questions"]) == 3

        for _ in range(3):
            result = client.post(
                f"/api/v1/interviews/sessions/{session_id}/answers",
                json={"answer": "In a React project, I built and tested a component, then measured the result."},
            )
            assert result.status_code == 200
        completed = result.json()
        assert completed["status"] == "completed"
        assert completed["total_score"] > 0
        assert completed["responses"][0]["evaluation_source"] == "local_rubric"
        assert client.get(f"/api/v1/interviews/sessions/{session_id}").status_code == 200
        assert client.post(
            f"/api/v1/interviews/sessions/{session_id}/answers",
            json={"answer": "I already completed the interview."},
        ).status_code == 409
    finally:
        if session_id is not None:
            db.query(InterviewSession).filter_by(id=session_id).delete()
        db.query(ResumeAnalysis).filter_by(id=analysis_id).delete()
        db.commit()
        db.close()