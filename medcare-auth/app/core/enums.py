import enum


class UserRole(str, enum.Enum):
    DOCTOR = "doctor"
    PHARMACIST = "pharmacist"
