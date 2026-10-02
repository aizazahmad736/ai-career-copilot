import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Any, Dict

from app.core.config import settings

TOKEN_LIFETIME_SECONDS = 12 * 60 * 60
PASSWORD_ITERATIONS = 310_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS)
    return f"pbkdf2_sha256${PASSWORD_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iteration_text, salt_text, expected = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_text), int(iteration_text)
        ).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def create_access_token(user_id: int, email: str) -> str:
    payload = _encode(json.dumps({
        "sub": user_id,
        "email": email,
        "exp": int(time.time()) + TOKEN_LIFETIME_SECONDS,
    }, separators=(",", ":")).encode("utf-8"))
    signature = _encode(hmac.new(settings.AUTH_SECRET.encode("utf-8"), payload.encode("ascii"), hashlib.sha256).digest())
    return f"{payload}.{signature}"


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload, signature = token.split(".", 1)
        expected = _encode(hmac.new(settings.AUTH_SECRET.encode("utf-8"), payload.encode("ascii"), hashlib.sha256).digest())
        if not hmac.compare_digest(signature, expected):
            raise ValueError("Invalid token signature")
        padded = payload + "=" * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(padded.encode("ascii")))
        if int(data["exp"]) <= int(time.time()):
            raise ValueError("Token expired")
        return data
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError("Invalid or expired access token") from error