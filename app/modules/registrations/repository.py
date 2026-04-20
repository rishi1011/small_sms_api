"""Repository layer for registration data access."""

from typing import Optional

from sqlalchemy.orm import Session

from app import crud
from app.modules.registrations.schemas import RegistrationCreate


class RegistrationRepository:
    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        school_year_id: Optional[int] = None,
        grade_id: Optional[int] = None,
        regi_no: Optional[str] = None,
    ):
        params = {
            "grade_id": grade_id,
            "school_year_id": school_year_id,
            "regi_no": regi_no,
        }
        return crud.registeration.get_multi(db, skip=skip, limit=limit, params=params)

    def get(self, db: Session, registration_id: int):
        return crud.registeration.get(db, registration_id)

    def get_current_school_year(self, db: Session):
        return crud.school_year.get_current_school_year(db)

    def get_student(self, db: Session, student_id: int):
        return crud.student.get(db, student_id)

    def get_grade(self, db: Session, grade_id: int):
        return crud.grade.get(db, grade_id)

    def find_student_registration_for_school_year(
        self, db: Session, student_id: int, school_year_id: int
    ):
        return crud.registeration.get_registration_by_grade_student_school_year(
            db, student_id=student_id, school_year_id=school_year_id
        )

    def generate_unique_regi_no(self, db: Session, school_year, grade):
        return crud.registeration.generate_unique_regi_no(db, school_year, grade)

    def create(self, db: Session, registration_in: RegistrationCreate):
        return crud.registeration.create(db, obj_in=registration_in)
