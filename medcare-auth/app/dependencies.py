from fastapi import HTTPException, Request, status

from app.core.enums import UserRole
from app.core.security import decode_access_token


def get_current_staff(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = auth_header.removeprefix("Bearer ").strip()

    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return {"username": payload["sub"], "role": payload["role"]}


def require_role(*allowed_roles: UserRole):
    def guard(request: Request) -> dict:
        staff = get_current_staff(request)
        if staff["role"] not in {role.value for role in allowed_roles}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Không đủ quyền hạn",
            )
        return staff

    return guard
