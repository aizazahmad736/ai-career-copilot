import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.job_search_service import job_search_service, strip_html
from app.services.job_matching_service import job_matching_service

client = TestClient(app)

CANDIDATE_SKILLS = {
    "languages": ["Python", "JavaScript", "SQL"],
    "frameworks": ["React.js", "FastAPI"],
    "databases": ["Postgres"],
    "tools_and_cloud": ["Git / GitHub", "Docker"],
    "core_concepts": ["REST APIs"],
    "soft_skills": ["Communication"],
}

def make_job(job_id, title, description, **overrides):
    job = {
        "id": job_id,
        "title": title,
        "company": f"Company {job_id}",
        "location": "Remote - Worldwide",
        "remote": True,
        "url": f"https://example.com/jobs/{job_id}",
        "source": "Remotive",
        "posted_at": None,
        "job_type": "Full Time",
        "salary": None,
        "tags": [],
        "description": description,
    }
    job.update(overrides)
    return job

FAKE_JOBS = [
    make_job("a", "Junior Full Stack Developer", "We use React, Python, FastAPI, PostgreSQL, Docker and Git."),
    make_job("b", "Senior Full Stack Engineer", "Kubernetes, Go, Kafka, AWS, Terraform and system design."),
    make_job("c", "Head Chef", "Run a busy kitchen and manage suppliers."),
    make_job("d", "Full Stack Developer", "React and Node.js with MongoDB.", location="Berlin", remote=False),
]

@pytest.fixture
def fake_providers(monkeypatch):
    job_search_service._cache.clear()
    monkeypatch.setattr(job_search_service, "_fetch_remotive", lambda query: list(FAKE_JOBS))
    monkeypatch.setattr(job_search_service, "_fetch_arbeitnow", lambda: [])

@pytest.fixture
def failing_providers(monkeypatch):
    def boom(*args, **kwargs):
        raise ConnectionError("network unavailable")
    job_search_service._cache.clear()
    monkeypatch.setattr(job_search_service, "_fetch_remotive", boom)
    monkeypatch.setattr(job_search_service, "_fetch_arbeitnow", boom)

def test_strip_html():
    assert strip_html("<p>Build <strong>APIs</strong> &amp; UIs</p><script>x()</script>") == "Build APIs & UIs"

def test_extract_skills_handles_symbols_and_lookalikes():
    skills = job_matching_service.extract_skills("We need C++, C#, Node.js, JavaScript and CI/CD. The rest is up to you.")
    assert "C++" in skills
    assert "C#" in skills
    assert "Node.js" in skills
    assert "JavaScript" in skills
    assert "CI/CD" in skills
    assert "Java" not in skills
    assert "REST APIs" not in skills

def test_candidate_skill_set_normalizes_aliases():
    found = job_matching_service.candidate_skill_set(CANDIDATE_SKILLS)
    assert {"React", "PostgreSQL", "Git", "Python"} <= found

def test_build_query():
    assert job_search_service.build_query("Frontend Developer") == "frontend developer"
    assert job_search_service.build_query("Junior Mobile Developer") == "mobile developer"

def test_web_query_uses_candidate_technical_skills_and_location():
    query = job_search_service._web_query(
        "full stack developer",
        "Entry-Level / Junior",
        "Berlin",
        CANDIDATE_SKILLS,
    )
    assert query == "junior full stack developer jobs Python JavaScript SQL React.js Berlin apply"
    assert "Communication" not in query

def test_web_provider_receives_cv_personalized_query(monkeypatch):
    job_search_service._cache.clear()
    observed_queries = []
    monkeypatch.setattr(job_search_service, "_fetch_remotive", lambda query: [])
    monkeypatch.setattr(job_search_service, "_fetch_arbeitnow", lambda: [])

    def fetch_tavily(query, api_key):
        observed_queries.append((query, api_key))
        return [make_job("web-1", "Junior Full Stack Developer", "React and Python")]

    monkeypatch.setattr(job_search_service, "_fetch_tavily", fetch_tavily)
    jobs, sources, errors, _, demo_mode = job_search_service.search(
        target_role="Junior Full Stack Developer",
        location="Berlin",
        tavily_api_key="test-key",
        skills=CANDIDATE_SKILLS,
    )

    assert observed_queries == [
        ("junior full stack developer jobs Python JavaScript SQL React.js Berlin apply", "test-key")
    ]
    assert len(jobs) == 1
    assert sources == ["Tavily"]
    assert errors == {}
    assert demo_mode is False

def test_rank_jobs_orders_and_filters():
    matches, total = job_matching_service.rank_jobs(FAKE_JOBS, CANDIDATE_SKILLS, "Junior Full Stack Developer")
    titles = [m.title for m in matches]
    assert titles[0] == "Junior Full Stack Developer"
    assert "Head Chef" not in titles
    assert total == 3

    top = matches[0]
    assert top.match_score >= 75
    assert top.fit_label == "Strong Match"
    assert "React" in top.matched_skills
    assert top.missing_skills == []

    senior = next(m for m in matches if m.title.startswith("Senior"))
    assert senior.match_score < top.match_score
    assert "Kubernetes" in senior.missing_skills

def test_rank_jobs_location_and_remote_filters():
    remote, _ = job_matching_service.rank_jobs(FAKE_JOBS, CANDIDATE_SKILLS, "Junior Full Stack Developer", remote_only=True)
    assert all(m.remote for m in remote)

    berlin, _ = job_matching_service.rank_jobs(FAKE_JOBS, CANDIDATE_SKILLS, "Junior Full Stack Developer", location="berlin")
    assert "Berlin" in [m.location for m in berlin]

def test_job_sources_endpoint():
    response = client.get("/api/v1/jobs/sources")
    assert response.status_code == 200
    names = [s["name"] for s in response.json()["sources"]]
    assert "Remotive" in names
    assert "Tavily" in names

def test_job_search_endpoint(fake_providers):
    response = client.post("/api/v1/jobs/search", json={
        "skills": CANDIDATE_SKILLS,
        "target_role": "Junior Full Stack Developer",
        "limit": 2,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["is_demo_mode"] is False
    assert data["sources_used"] == ["Remotive"]
    assert data["total_found"] == 3
    assert len(data["jobs"]) == 2
    assert data["jobs"][0]["match_score"] >= data["jobs"][1]["match_score"]
    assert data["id"] is not None

def test_job_search_falls_back_to_samples(failing_providers):
    response = client.post("/api/v1/jobs/search", json={
        "skills": CANDIDATE_SKILLS,
        "target_role": "Junior Full Stack Developer",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["is_demo_mode"] is True
    assert data["sources_used"] == ["Sample"]
    assert set(data["source_errors"]) == {"Remotive", "Arbeitnow"}
    assert len(data["jobs"]) > 0
