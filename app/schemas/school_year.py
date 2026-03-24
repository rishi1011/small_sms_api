from datetime import date
from datetime import datetime
from pydantic import (
    BaseModel,
    ValidationInfo,
    field_validator,
    ConfigDict,
)


class Base(BaseModel):
    title: str
    start_date: date
    end_date: date

    @field_validator("title")
    def validate_title(cls, value):
        if not value:
            raise ValueError('Title must not be empty.')
        return value

    @field_validator("end_date")
    def validate_start_and_end_date(cls, v, info: ValidationInfo):
        if info.data['start_date'] >= v:
            raise ValueError('End date must be after start date.')
        return v
    
    @field_validator("start_date", "end_date", mode="before")
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        return datetime.strptime(value, "%Y-%m-%d").date()


class SchoolYearCreate(Base):
    pass


class SchoolYearUpdate(Base):
    pass


class SchoolYearInDB(Base):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
