"""Service layer for school year business logic."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.school_years.repository import SchoolYearRepository
from app.modules.school_years.schemas import SchoolYearCreate, SchoolYearUpdate


class SchoolYearService:
    def __init__(self, repository: SchoolYearRepository | None = None):
        self.repository = repository or SchoolYearRepository()

    def get_school_years(self, db: Session, skip: int = 0, limit: int = 20):
        return self.repository.get_multi(db, skip=skip, limit=limit)

    def get_school_year(self, db: Session, school_year_id: int):
        school_year = self.repository.get(db, school_year_id)
        if not school_year:
            raise HTTPException(
                status_code=404,
                detail=f"School year with id {school_year_id} does not exist",
            )
        return school_year

    def create_school_year(self, db: Session, school_year_in: SchoolYearCreate):
        school_year = self.repository.get_by_name(db, title=school_year_in.title)
        if school_year:
            raise HTTPException(
                status_code=409, detail="A school year with this name already exists"
            )
        return self.repository.create(db, school_year_in=school_year_in)

    def update_school_year(
        self, db: Session, school_year_id: int, school_year_in: SchoolYearUpdate
    ):
        school_year = self.repository.get(db, school_year_id)
        if not school_year:
            raise HTTPException(
                status_code=404,
                detail=f"School year with id {school_year_id} does not exist",
            )
        return self.repository.update(db, db_obj=school_year, school_year_in=school_year_in)

    def activate_school_year(self, db: Session, school_year_id: int):
        school_year = self.repository.get(db, school_year_id)
        if not school_year:
            raise HTTPException(
                status_code=404,
                detail=f"School year with id {school_year_id} does not exist",
            )
        return self.repository.activate(db, school_year_id=school_year_id)

    def delete_school_year(self, db: Session, school_year_id: int):
        school_year = self.repository.get(db, school_year_id)
        if not school_year:
            raise HTTPException(
                status_code=404,
                detail=f"School year with id {school_year_id} does not exist",
            )
        if school_year.students:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"لايمكن حذف هذا العالم الدراسي {school_year.title} لانه توجد بيانات طلاب مرتبطة به, يجب حذف بيانات الطلاب اولاُ ثم حاول مرة اخرى.",
            )
        self.repository.remove(db, school_year_id=school_year_id)
