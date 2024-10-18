from typing import Optional
from pydantic import BaseModel, Field

class DoctorSchema(BaseModel):
    firstName: str = Field(...)
    lastName: str = Field(...)
    specialty: str = Field(...)
    contactNumber: str = Field(...)
    experienceYears: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName":"Doe",
                "specialty":"Radiology",
                "contactNumber": "+221773940225",
                "experienceYears": 10,
            }
        }


class UpdateDoctorModel(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] =  None
    contactNumber: Optional[str] =  None
    experienceYears: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName":"Doe",
                "contactNumber":"+221773940225",
                "experienceYears": 5
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}