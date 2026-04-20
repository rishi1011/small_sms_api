"""Repository layer for grade data access."""

from sqlalchemy.orm import Session

from app import crud
from app.modules.grades.schemas import (
    GradeCreate,
    GradeSubjectCreate,
    GradeSubjectUpdate,
    GradeUpdate,
)


class GradeRepository:
    def get_multi(self, db: Session, skip: int = 0, limit: int = 20):
        return crud.grade.get_multi(db, skip=skip, limit=limit)

    def get(self, db: Session, grade_id: int):
        return crud.grade.get(db, id=grade_id)

    def get_by_name(self, db: Session, name: str):
        return crud.grade.get_by_name(db, name=name)

    def create(self, db: Session, grade_in: GradeCreate):
        return crud.grade.create(db, obj_in=grade_in)

    def update(self, db: Session, db_obj, grade_in: GradeUpdate):
        return crud.grade.update(db, db_obj=db_obj, obj_in=grade_in)

    def remove(self, db: Session, grade_id: int):
        return crud.grade.remove(db, id=grade_id)

    def get_grade_subject(self, db: Session, grade_id: int, subject_id: int):
        return crud.grade_subject.get(db, grade_id, subject_id)

    def create_grade_subject(self, db: Session, grade_subject_in: GradeSubjectCreate):
        return crud.grade_subject.create(db, obj_in=grade_subject_in)

    def update_grade_subject(
        self, db: Session, db_obj, grade_subject_in: GradeSubjectUpdate
    ):
        return crud.grade_subject.update(db, db_obj=db_obj, obj_in=grade_subject_in)

    def remove_grade_subject(self, db: Session, grade_id: int, subject_id: int):
        return crud.grade_subject.remove(db, grade_id=grade_id, subject_id=subject_id)

    def get_subject(self, db: Session, subject_id: int):
        return crud.subject.get(db, subject_id)

    def get_assigned_or_not_assigned_subjects(
        self, db: Session, grade_id: int, assigned: bool
    ):
        return crud.grade.get_grade_assigned_or_not_assigned_subjects(
            db, grade_id=grade_id, assigned=assigned
        )
