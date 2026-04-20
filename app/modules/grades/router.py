"""Router for grade module endpoints."""

from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.modules.grades.schemas import (
    GradeCreate,
    GradeInDB,
    GradeSubjectCreate,
    GradeSubjectOut,
    GradeSubjectsOut,
    GradeSubjectUpdate,
    GradeUpdate,
)
from app.modules.grades.service import GradeService

router = APIRouter(prefix="/grades", tags=["Grades"])
service = GradeService()


@router.get("", response_model=List[GradeInDB])
def get_grades(*, db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    return service.get_grades(db, skip=skip, limit=limit)


@router.get("/{grade_id}", response_model=GradeInDB)
def get_grade(*, db: Session = Depends(get_db), grade_id: int):
    return service.get_grade(db, grade_id=grade_id)


@router.post("", response_model=GradeInDB, status_code=status.HTTP_201_CREATED)
def create_grade(*, db: Session = Depends(get_db), grade_in: GradeCreate):
    return service.create_grade(db, grade_in=grade_in)


@router.put("/{grade_id}", response_model=GradeInDB)
def update_grade(*, db: Session = Depends(get_db), grade_id: int, grade_in: GradeUpdate):
    return service.update_grade(db, grade_id=grade_id, grade_in=grade_in)


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(*, db: Session = Depends(get_db), grade_id: int):
    service.delete_grade(db, grade_id=grade_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/subjects", response_model=GradeSubjectOut)
def assign_subject_to_grade(
    *, db: Session = Depends(get_db), grade_subject_in: GradeSubjectCreate
):
    return service.assign_subject_to_grade(db, grade_subject_in=grade_subject_in)


@router.get("/{grade_id}/subjects", response_model=GradeSubjectsOut)
def get_assigned_or_not_assigned_grade_subjects(
    *, db: Session = Depends(get_db), grade_id: int, assigned: bool = True
):
    return service.get_assigned_or_not_assigned_grade_subjects(
        db, grade_id=grade_id, assigned=assigned
    )


@router.put("/{grade_id}/subjects/{subject_id}", response_model=GradeSubjectOut)
def update_grade_subject(
    *,
    db: Session = Depends(get_db),
    grade_id: int,
    subject_id: int,
    grade_subject_in: GradeSubjectUpdate,
):
    return service.update_grade_subject(
        db,
        grade_id=grade_id,
        subject_id=subject_id,
        grade_subject_in=grade_subject_in,
    )


@router.delete("/{grade_id}/subjects/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def unassign_subject_from_grade(
    *,
    db: Session = Depends(get_db),
    grade_id: int,
    subject_id: int,
):
    service.unassign_subject_from_grade(db, grade_id=grade_id, subject_id=subject_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
