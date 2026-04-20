"""Student router scaffold for module-based architecture."""

from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import CommonQueryParams, get_db
from app.modules.students.schemas import StudentCreate, StudentInDB, StudentUpdate
from app.modules.students.service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])


def get_student_service() -> StudentService:
    return StudentService()


@router.get("", response_model=List[StudentInDB])
def get_students(
    *,
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service),
    commons: CommonQueryParams = Depends(),
):
    return service.get_students(db, skip=commons.skip, limit=commons.limit)


@router.get("/{student_id}", response_model=StudentInDB)
def get_student(
    *,
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service),
    student_id: int,
):
    return service.get_student(db, student_id=student_id)


@router.post("", response_model=StudentInDB, status_code=status.HTTP_201_CREATED)
def create_student(
    *,
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service),
    student_in: StudentCreate,
):
    return service.create_student(db, student_in=student_in)


@router.put("/{student_id}", response_model=StudentInDB)
def update_student(
    *,
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service),
    student_id: int,
    student_in: StudentUpdate,
):
    return service.update_student(db, student_id=student_id, student_in=student_in)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    *,
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service),
    student_id: int,
):
    service.delete_student(db, student_id=student_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
