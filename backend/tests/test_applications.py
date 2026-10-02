from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.main import app
from app.models.application import Application

client = TestClient(app)


def test_save_and_update_application_status():
    job_key = "test-job:unique-application"
    try:
        response = client.post("/api/v1/applications", json={
            "job_key": job_key,
            "title": "Junior Developer",
            "company": "Test Co",
            "url": "https://example.com/jobs/1",
            "target_role": "Backend Developer",
        })
        assert response.status_code == 200
        application_id = response.json()["id"]
        duplicate = client.post("/api/v1/applications", json={
            "job_key": job_key,
            "title": "Junior Developer",
            "company": "Test Co",
            "url": "https://example.com/jobs/1",
        })
        assert duplicate.json()["id"] == application_id
        updated = client.patch(f"/api/v1/applications/{application_id}", json={"status": "applied", "notes": "Applied today"})
        assert updated.status_code == 200
        assert updated.json()["status"] == "applied"
        assert updated.json()["notes"] == "Applied today"
    finally:
        db = SessionLocal()
        db.query(Application).filter_by(job_key=job_key, user_id=None).delete()
        db.commit()
        db.close()