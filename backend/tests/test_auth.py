from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.main import app
from app.models.user import User

client = TestClient(app)


def test_register_login_and_signed_access_token():
    email = f"career-{uuid4().hex}@example.com"
    password = "a-long-test-password-123"
    user_id = None
    try:
        registered = client.post("/api/v1/auth/register", json={"email": email, "password": password})
        assert registered.status_code == 201
        token = registered.json()["access_token"]
        user_id = registered.json()["user"]["id"]
        profile = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert profile.status_code == 200
        assert profile.json()["email"] == email

        login = client.post("/api/v1/auth/login", json={"email": email.upper(), "password": password})
        assert login.status_code == 200
        assert client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid"}).status_code == 401
        assert client.post("/api/v1/auth/register", json={"email": email, "password": password}).status_code == 409
    finally:
        if user_id is not None:
            db = SessionLocal()
            db.query(User).filter_by(id=user_id).delete()
            db.commit()
            db.close()