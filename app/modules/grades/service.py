"""Service layer for grade business logic."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.grades.repository import GradeRepository
from app.modules.grades.schemas import (
    GradeCreate,
    GradeSubjectCreate,
    GradeSubjectUpdate,
    GradeUpdate,
)


class GradeService:
    def __init__(self, repository: GradeRepository | None = None):
        self.repository = repository or GradeRepository()

    def get_grades(self, db: Session, skip: int = 0, limit: int = 20):
        return self.repository.get_multi(db, skip=skip, limit=limit)

    def get_grade(self, db: Session, grade_id: int):
        grade = self.repository.get(db, grade_id)
        if not grade:
            raise HTTPException(
                status_code=404,
                detail=f"Grade with id {grade_id} does not exist",
            )
        return grade

    def create_grade(self, db: Session, grade_in: GradeCreate):
        grade = self.repository.get_by_name(db, name=grade_in.name)
        if grade:
            raise HTTPException(
                status_code=409,
                detail="A grade with this name already exists",
            )
        return self.repository.create(db, grade_in=grade_in)

    def update_grade(self, db: Session, grade_id: int, grade_in: GradeUpdate):
        grade = self.repository.get(db, grade_id)
        if not grade:
            raise HTTPException(
                status_code=404,
                detail=f"Grade with id {grade_id} does not exist",
            )
        return self.repository.update(db, db_obj=grade, grade_in=grade_in)

    def delete_grade(self, db: Session, grade_id: int):
        grade = self.repository.get(db, grade_id)
        if not grade:
            raise HTTPException(
                status_code=404,
                detail=f"There is no grade with id {grade_id}.",
            )
        if grade.subjects:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot delete {grade.name} because there are subjects linked to this grade, you must unassign all subjects linked to the grade and then try again.",
            )
        if grade.students:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot delete {grade.name} because there is student data linked to this grade, you must first delete the student data linked to this grade and then try again.",
            )
        self.repository.remove(db, grade_id=grade_id)

    def assign_subject_to_grade(self, db: Session, grade_subject_in: GradeSubjectCreate):
        grade = self.repository.get(db, grade_subject_in.grade_id)
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grade with id {grade_subject_in.grade_id} does not exist",
            )

        subject = self.repository.get_subject(db, grade_subject_in.subject_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subject with id {grade_subject_in.subject_id} does not exist",
            )

        grade_subject = self.repository.get_grade_subject(
            db, grade_subject_in.grade_id, grade_subject_in.subject_id
        )
        if grade_subject:
            raise HTTPException(
                status_code=409,
                detail=f"{grade_subject.subject.name} has already assigned to {grade_subject.grade.name}",
            )

        self.repository.create_grade_subject(db, grade_subject_in=grade_subject_in)
        return {"grade": grade, "subject": subject}

    def get_assigned_or_not_assigned_grade_subjects(
        self, db: Session, grade_id: int, assigned: bool = True
    ):
        grade = self.repository.get(db, grade_id)
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grade with id {grade_id} does not exist",
            )
        subjects = self.repository.get_assigned_or_not_assigned_subjects(
            db, grade_id=grade_id, assigned=assigned
        )
        return {"grade": grade, "subjects": subjects}

    def update_grade_subject(
        self,
        db: Session,
        grade_id: int,
        subject_id: int,
        grade_subject_in: GradeSubjectUpdate,
    ):
        db_obj = self.repository.get_grade_subject(db, grade_id, subject_id)
        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Grade with id {grade_id} or Subject with {subject_id} does not exist",
            )
        return self.repository.update_grade_subject(
            db, db_obj=db_obj, grade_subject_in=grade_subject_in
        )

    def unassign_subject_from_grade(self, db: Session, grade_id: int, subject_id: int):
        grade = self.repository.get(db, grade_id)
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grade with id {grade_id} does not exist",
            )
        subject = self.repository.get_subject(db, subject_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subject with id {subject_id} does not exist",
            )
        grade_subject = self.repository.get_grade_subject(db, grade_id, subject_id)
        if not grade_subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{subject.name} is not assigned to {grade.name}.",
            )
        self.repository.remove_grade_subject(db, grade_id=grade_id, subject_id=subject_id)
