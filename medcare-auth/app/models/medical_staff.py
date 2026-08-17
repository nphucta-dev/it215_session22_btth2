from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import UserRole
from app.database import Base


class MedicalStaff(Base):
    __tablename__ = "medical_staff"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
