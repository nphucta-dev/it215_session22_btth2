from pydantic import BaseModel, ConfigDict, Field


class PrescriptionCreateRequest(BaseModel):
    patient_name: str = Field(min_length=1, max_length=100)
    medication: str = Field(min_length=1, max_length=255)


class PrescriptionResponse(BaseModel):
    id: int
    patient_name: str
    medication: str
    issued_by: str

    model_config = ConfigDict(from_attributes=True)
