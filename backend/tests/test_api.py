import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.parser_service import parser_service
from app.services.skill_gap_service import skill_gap_service

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "AI Career Copilot" in data["service"]

def test_get_roles():
    response = client.get("/api/v1/cv/roles")
    assert response.status_code == 200
    data = response.json()
    assert "roles" in data
    assert len(data["roles"]) > 0
    role_names = [r["name"] for r in data["roles"]]
    assert "Junior Full Stack Developer" in role_names

def test_parser_service():
    sample_txt = b"John Doe\nSoftware Engineer\nPython, JavaScript, React, SQL"
    text, file_type = parser_service.parse_file(sample_txt, "resume.txt")
    assert file_type == "txt"
    assert "John Doe" in text
    assert "Python" in text

def test_skill_gap_service():
    skills = {
        "languages": ["Python", "JavaScript"],
        "frameworks": ["React", "FastAPI"],
        "databases": ["PostgreSQL"],
        "tools_and_cloud": ["Git", "Docker"]
    }
    score, matched, partial, missing, bonus, recommendations = skill_gap_service.evaluate_gaps(
        extracted_skills=skills,
        target_role="Junior Full Stack Developer"
    )
    assert score > 50.0
    matched_skills = [m.skill for m in matched]
    assert "Python" in matched_skills
    assert "JavaScript" in matched_skills
    assert len(recommendations) > 0

def test_analyze_sample_endpoint():
    response = client.post("/api/v1/cv/analyze-sample", data={"target_role": "Junior Full Stack Developer"})
    assert response.status_code == 200
    data = response.json()
    assert data["target_role"] == "Junior Full Stack Developer"
    assert data["match_score"] > 50
    assert len(data["matched_skills"]) > 0
    assert "parsed_resume" in data
    assert "ats_feedback" in data
    assert "recommendations" in data
