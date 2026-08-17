from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_name: Mapped[str] = mapped_column(String(100), nullable=False)
    medication: Mapped[str] = mapped_column(String(255), nullable=False)
    issued_by: Mapped[str] = mapped_column(String(50), nullable=False)
