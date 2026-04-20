"""Router for nationality module endpoints."""

from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.modules.nationalities.schemas import (
    NationalityCreate,
    NationalityInDB,
    NationalityUpdate,
)
from app.modules.nationalities.service import NationalityService

router = APIRouter(prefix="/nationalities", tags=["Nationalities"])


def get_nationality_service() -> NationalityService:
    return NationalityService()


@router.get("", response_model=List[NationalityInDB])
def get_nationalities(
    *,
    db: Session = Depends(deps.get_db),
    service: NationalityService = Depends(get_nationality_service),
    commons: deps.CommonQueryParams = Depends(),
):
    return service.get_nationalities(db, skip=commons.skip, limit=commons.limit)


@router.get("/{nationality_id}", response_model=NationalityInDB)
def get_nationality(
    *,
    db: Session = Depends(deps.get_db),
    service: NationalityService = Depends(get_nationality_service),
    nationality_id: int,
):
    return service.get_nationality(db, nationality_id=nationality_id)


@router.post("", response_model=NationalityInDB, status_code=status.HTTP_201_CREATED)
def create_nationality(
    *,
    db: Session = Depends(deps.get_db),
    service: NationalityService = Depends(get_nationality_service),
    nationality_in: NationalityCreate,
):
    return service.create_nationality(db, nationality_in=nationality_in)


@router.put("/{nationality_id}", response_model=NationalityInDB)
def update_nationality(
    *,
    db: Session = Depends(deps.get_db),
    service: NationalityService = Depends(get_nationality_service),
    nationality_id: int,
    nationality_in: NationalityUpdate,
):
    return service.update_nationality(
        db, nationality_id=nationality_id, nationality_in=nationality_in
    )


@router.delete("/{nationality_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nationality(
    *,
    db: Session = Depends(deps.get_db),
    service: NationalityService = Depends(get_nationality_service),
    nationality_id: int,
):
    service.delete_nationality(db, nationality_id=nationality_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
