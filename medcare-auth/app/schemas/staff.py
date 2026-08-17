from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import UserRole


class StaffRegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    role: UserRole


class StaffLoginRequest(BaseModel):
    username: str
    password: str


class StaffResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
