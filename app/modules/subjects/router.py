"""Router for subject module endpoints."""

from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.modules.subjects.schemas import SubjectCreate, SubjectInDB, SubjectUpdate
from app.modules.subjects.service import SubjectService

router = APIRouter(prefix="/subjects", tags=["Subjects"])
service = SubjectService()


@router.get("", response_model=List[SubjectInDB])
def get_subjects(*, db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    return service.get_subjects(db, skip=skip, limit=limit)


@router.get("/{subject_id}", response_model=SubjectInDB)
def get_subject(*, db: Session = Depends(get_db), subject_id: int):
    return service.get_subject(db, subject_id=subject_id)


@router.post("", response_model=SubjectInDB, status_code=status.HTTP_201_CREATED)
def create_subject(*, db: Session = Depends(get_db), subject_in: SubjectCreate):
    return service.create_subject(db, subject_in=subject_in)


@router.put("/{subject_id}", response_model=SubjectInDB)
def update_subject(
    *, db: Session = Depends(get_db), subject_id: int, subject_in: SubjectUpdate
):
    return service.update_subject(db, subject_id=subject_id, subject_in=subject_in)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(*, db: Session = Depends(get_db), subject_id: int):
    service.delete_subject(db, subject_id=subject_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
