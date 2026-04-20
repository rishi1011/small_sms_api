"""Service layer for registration business logic."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.registrations.repository import RegistrationRepository
from app.modules.registrations.schemas import RegistrationCreate, RegistrationIn


class RegistrationService:
    def __init__(self, repository: RegistrationRepository | None = None):
        self.repository = repository or RegistrationRepository()

    def get_registrations(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        school_year_id: Optional[int] = None,
        grade_id: Optional[int] = None,
        regi_no: Optional[str] = None,
    ):
        return self.repository.get_multi(
            db,
            skip=skip,
            limit=limit,
            school_year_id=school_year_id,
            grade_id=grade_id,
            regi_no=regi_no,
        )

    def get_registration(self, db: Session, registration_id: int):
        registration = self.repository.get(db, registration_id)
        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registration with id {registration_id} does not exist.",
            )
        return registration

    def create_registration(self, db: Session, registration_in: RegistrationIn):
        school_year = self.repository.get_current_school_year(db)
        if not school_year:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="School year not set yet! Please go to settings and set it.",
            )

        student = self.repository.get_student(db, registration_in.student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with id {registration_in.student_id} does not exist.",
            )

        grade = self.repository.get_grade(db, registration_in.grade_id)
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grade with id {registration_in.grade_id} does not exist.",
            )

        reg = self.repository.find_student_registration_for_school_year(
            db, student_id=student.id, school_year_id=school_year.id
        )
        if reg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot register student in two classes on the same year.",
            )

        regi_no = self.repository.generate_unique_regi_no(db, school_year, grade)
        registration_data = RegistrationCreate(
            regi_no=regi_no,
            student_id=student.id,
            grade_id=grade.id,
            school_year_id=school_year.id,
        )
        return self.repository.create(db, registration_in=registration_data)
