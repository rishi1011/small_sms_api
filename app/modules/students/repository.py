"""Repository layer for student data access."""

from sqlalchemy.orm import Session

from app import crud
from app.modules.students.schemas import StudentCreate, StudentUpdate


class StudentRepository:
    """Thin wrapper around existing CRUD to support module migration."""

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return crud.student.get_multi(db, skip=skip, limit=limit)

    def get(self, db: Session, student_id: int):
        return crud.student.get(db, student_id)

    def create(self, db: Session, student_in: StudentCreate):
        return crud.student.create(db, obj_in=student_in)

    def update(self, db: Session, db_obj, student_in: StudentUpdate):
        return crud.student.update(db, db_obj=db_obj, obj_in=student_in)

    def remove(self, db: Session, student_id: int):
        return crud.student.remove(db, id=student_id)
