"""Router for school year module endpoints."""

from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.modules.school_years.schemas import (
    SchoolYearCreate,
    SchoolYearInDB,
    SchoolYearUpdate,
)
from app.modules.school_years.service import SchoolYearService

router = APIRouter(prefix="/school-years", tags=["School Years"])


def get_school_year_service() -> SchoolYearService:
    return SchoolYearService()


@router.get("", response_model=List[SchoolYearInDB])
def get_school_years(
    *,
    db: Session = Depends(get_db),
    service: SchoolYearService = Depends(get_school_year_service),
    skip: int = 0,
    limit: int = 20,
):
    return service.get_school_years(db, skip=skip, limit=limit)


@router.get("/{school_year_id}", response_model=SchoolYearInDB)
def get_school_year(
    *,
    db: Session = Depends(get_db),
    service: SchoolYearService = Depends(get_school_year_service),
    school_year_id: int,
):
    return service.get_school_year(db, school_year_id=school_year_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_school_year(
    *,
    db: Session = Depends(get_db),
    service: SchoolYearService = Depends(get_school_year_service),
    school_year_in: SchoolYearCreate,
):
    return service.create_school_year(db, school_year_in=school_year_in)


@router.put("/{school_year_id}", response_model=SchoolYearInDB)
def update_school_year(
    *,
    db: Session = Depends(get_db),
    service: SchoolYearService = Depends(get_school_year_service),
    school_year_id: int,
    school_year_in: SchoolYearUpdate,
):
    return service.update_school_year(
        db, school_year_id=school_year_id, school_year_in=school_year_in
    )


@router.put("/{school_year_id}/activate", response_model=SchoolYearInDB)
def activate_school_year(
    *,
    db: Session = Depends(get_db),
    service: SchoolYearService = Depends(get_school_year_service),
    school_year_id: int,
):
    return service.activate_school_year(db, school_year_id=school_year_id)


@router.delete("/{school_year_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school_year(
    *,
    db: Session = Depends(get_db),
    service: SchoolYearService = Depends(get_school_year_service),
    school_year_id: int,
):
    service.delete_school_year(db, school_year_id=school_year_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
