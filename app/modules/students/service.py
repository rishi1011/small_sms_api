"""Service layer for student business logic."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.modules.students.repository import StudentRepository
from app.modules.students.schemas import StudentCreate, StudentUpdate


class StudentService:
    def __init__(self, repository: StudentRepository | None = None):
        self.repository = repository or StudentRepository()

    def get_students(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repository.get_multi(db, skip=skip, limit=limit)

    def get_student(self, db: Session, student_id: int):
        student = self.repository.get(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with id {student_id} does not exist.",
            )
        return student

    def create_student(self, db: Session, student_in: StudentCreate):
        if not crud.nationality.get(db, student_in.nationality_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nationality with id {student_in.nationality_id} not found.",
            )
        return self.repository.create(db, student_in=student_in)

    def update_student(self, db: Session, student_id: int, student_in: StudentUpdate):
        student = self.repository.get(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with id {student_id} does not exist.",
            )
        if not crud.nationality.get(db, student_in.nationality_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nationality with id {student_in.nationality_id} not found.",
            )
        return self.repository.update(db, db_obj=student, student_in=student_in)

    def delete_student(self, db: Session, student_id: int) -> None:
        student = self.repository.get(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with id {student_id} does not exist.",
            )
        if student.registrations:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete this student because, it has data depends on it.",
            )
        self.repository.remove(db, student_id=student_id)
