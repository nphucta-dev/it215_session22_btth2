from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.medical_staff import MedicalStaff
from app.schemas.staff import StaffLoginRequest, StaffRegisterRequest


def register_staff(db: Session, payload: StaffRegisterRequest) -> MedicalStaff:
    existing = db.execute(
        select(MedicalStaff).where(MedicalStaff.username == payload.username)
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    staff = MedicalStaff(
        username=payload.username,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(staff)
    db.flush()
    db.refresh(staff)
    return staff


def authenticate_staff(db: Session, payload: StaffLoginRequest) -> tuple[str, int]:
    staff = db.execute(
        select(MedicalStaff).where(MedicalStaff.username == payload.username)
    ).scalar_one_or_none()

    if not staff or not verify_password(payload.password, staff.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin đăng nhập không chính xác",
        )

    return create_access_token(subject=staff.username, role=staff.role)
