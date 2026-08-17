from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.database import get_db
from app.dependencies import require_role
from app.schemas.prescription import PrescriptionCreateRequest, PrescriptionResponse
from app.services.prescription_service import create_prescription, list_prescriptions
from app.utils.response import build_response

router = APIRouter(prefix="/api/v1/prescriptions", tags=["prescriptions"])


@router.post("")
def create(
    request: Request,
    payload: PrescriptionCreateRequest,
    db: Session = Depends(get_db),
    staff: dict = Depends(require_role(UserRole.DOCTOR)),
):
    prescription = create_prescription(db, payload, issued_by=staff["username"])
    return build_response(
        request,
        status.HTTP_201_CREATED,
        data=PrescriptionResponse.model_validate(prescription).model_dump(),
        message="Tạo đơn thuốc thành công",
    )


@router.get("/view")
def view(
    request: Request,
    db: Session = Depends(get_db),
    staff: dict = Depends(require_role(UserRole.DOCTOR, UserRole.PHARMACIST)),
):
    prescriptions = list_prescriptions(db)
    data = [PrescriptionResponse.model_validate(p).model_dump() for p in prescriptions]
    return build_response(
        request,
        status.HTTP_200_OK,
        data=data,
        message="Lấy danh sách đơn thuốc thành công",
    )
