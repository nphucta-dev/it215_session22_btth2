from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.prescription import Prescription
from app.schemas.prescription import PrescriptionCreateRequest


def create_prescription(
    db: Session, payload: PrescriptionCreateRequest, issued_by: str
) -> Prescription:
    prescription = Prescription(
        patient_name=payload.patient_name,
        medication=payload.medication,
        issued_by=issued_by,
    )
    db.add(prescription)
    db.flush()
    db.refresh(prescription)
    return prescription


def list_prescriptions(db: Session) -> list[Prescription]:
    return list(db.execute(select(Prescription)).scalars().all())
