import re
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.student import GenderEnum
from app.schemas.nationality import NationalityInDB

PHONE_PATTERN = re.compile(r"^\d{9}$")


class Base(BaseModel):
    first_name: str
    father_name: str
    gfather_name: str
    last_name: str
    gender: GenderEnum
    date_of_birth: date
    guardian_phone_no: str

    @classmethod
    def _validate_required_text(cls, value: str, label: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError(f"{label} must not be empty.")
        return value

    @field_validator("first_name", "father_name", "gfather_name", "last_name")
    def validate_names(cls, value: str, info):
        labels = {
            "first_name": "First name",
            "father_name": "Father name",
            "gfather_name": "Grand Father name",
            "last_name": "Last name",
        }
        return cls._validate_required_text(value, labels[info.field_name])

    @field_validator("date_of_birth", mode="before")
    def parse_date_of_birth(cls, value):
        if isinstance(value, date):
            return value
        return datetime.strptime(value, "%Y-%m-%d").date()

    @field_validator("guardian_phone_no")
    def validate_guardian_phone_no(cls, value: str):
        value = cls._validate_required_text(value, "Guardian phone number")
        if not PHONE_PATTERN.match(value):
            raise ValueError("Please Enter a valid phone number.")

        return value


class StudentCreate(Base):
    nationality_id: int


class StudentUpdate(StudentCreate):
    pass


class StudentInDB(Base):
    id: int
    nationality: NationalityInDB

    model_config = ConfigDict(from_attributes=True)
