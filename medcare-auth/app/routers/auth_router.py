from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.staff import StaffLoginRequest, StaffRegisterRequest, StaffResponse, TokenResponse
from app.services.auth_service import authenticate_staff, register_staff
from app.utils.response import build_response

router = APIRouter(prefix="/api/v1/medical", tags=["auth"])


@router.post("/register")
def register(request: Request, payload: StaffRegisterRequest, db: Session = Depends(get_db)):
    staff = register_staff(db, payload)
    return build_response(
        request,
        status.HTTP_201_CREATED,
        data=StaffResponse.model_validate(staff).model_dump(),
        message="Đăng ký nhân viên y tế thành công",
    )


@router.post("/login")
def login(request: Request, payload: StaffLoginRequest, db: Session = Depends(get_db)):
    token, expires_in = authenticate_staff(db, payload)
    token_data = TokenResponse(access_token=token, expires_in=expires_in)
    return build_response(
        request,
        status.HTTP_200_OK,
        data=token_data.model_dump(),
        message="Đăng nhập thành công",
    )
