from typing import Optional
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)


class Base(BaseModel):
    masculine_form: str
    feminine_form: str
    notes: Optional[str] = None

    @field_validator("masculine_form")
    def validate_masculine_form(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError('Masculine form must not be empty.')
        return value

    @field_validator("feminine_form")
    def validate_feminine_form(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError('Feminine form must not be empty.')
        return value


class NationalityCreate(Base):
    pass


class NationalityUpdate(Base):
    pass


class NationalityInDB(Base):
    id: int

    model_config = ConfigDict(from_attributes=True)
