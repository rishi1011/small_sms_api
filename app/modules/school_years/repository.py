"""Repository layer for school year data access."""

from sqlalchemy.orm import Session

from app import crud
from app.modules.school_years.schemas import SchoolYearCreate, SchoolYearUpdate


class SchoolYearRepository:
    def get_multi(self, db: Session, skip: int = 0, limit: int = 20):
        return crud.school_year.get_multi(db, skip=skip, limit=limit)

    def get(self, db: Session, school_year_id: int):
        return crud.school_year.get(db, id=school_year_id)

    def get_by_name(self, db: Session, title: str):
        return crud.school_year.get_by_name(db, name=title)

    def create(self, db: Session, school_year_in: SchoolYearCreate):
        return crud.school_year.create(db, obj_in=school_year_in)

    def update(self, db: Session, db_obj, school_year_in: SchoolYearUpdate):
        return crud.school_year.update(db, db_obj=db_obj, obj_in=school_year_in)

    def activate(self, db: Session, school_year_id: int):
        return crud.school_year.acivate_school_year(db, school_year_id)

    def remove(self, db: Session, school_year_id: int):
        return crud.school_year.remove(db, id=school_year_id)
