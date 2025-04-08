from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class ForeignLanguageCertificateBase(BaseModel):
    language: str = Field(..., max_length=50) 
    certificate_type: str = Field(..., max_length=50)
    level: str = Field(..., max_length=10)
    series_and_number: str = Field(..., max_length=50)
    date_of_issue: date



class ForeignLanguageCertificateCreate(ForeignLanguageCertificateBase):
    pass


class ForeignLanguageCertificateUpdate(BaseModel):
    language: str | None = Field(default=None, max_length=50) # Use | None for optional
    certificate_type: str | None = Field(default=None, max_length=50)
    level: str | None = Field(default=None, max_length=10)
    series_and_number: str | None = Field(default=None, max_length=50)
    date_of_issue: date | None = None



class ForeignLanguageCertificateResponse(ForeignLanguageCertificateBase):
    id: int
    file_path: str
    model_config = ConfigDict(from_attributes=True)
