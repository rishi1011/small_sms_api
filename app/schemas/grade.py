from typing import List
from pydantic import BaseModel, ConfigDict


class GradeBase(BaseModel):
    name: str
    numeric_value: int


class GradeCreate(GradeBase):
    pass


class GradeUpdate(GradeBase):
    pass


class GradeInDB(GradeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
