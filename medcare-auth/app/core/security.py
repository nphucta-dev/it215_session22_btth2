from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from jwt import PyJWTError

from app.core.config import settings
from app.core.enums import UserRole


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(subject: str, role: UserRole) -> tuple[str, int]:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": subject,
        "role": role.value,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    token = jwt.encode(
        payload, settings.medcare_secret_key, algorithm=settings.jwt_algorithm
    )
    expires_in = settings.access_token_expire_minutes * 60
    return token, expires_in


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token, settings.medcare_secret_key, algorithms=[settings.jwt_algorithm]
        )
    except PyJWTError as exc:
        raise ValueError("Invalid or expired token") from exc
