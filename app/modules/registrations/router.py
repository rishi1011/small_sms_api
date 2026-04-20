"""Router for registration module endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import CommonQueryParams, get_db
from app.modules.registrations.schemas import RegistrationIn, RegistrationOut
from app.modules.registrations.service import RegistrationService

router = APIRouter(prefix="/registrations", tags=["Registrations"])


def get_registration_service() -> RegistrationService:
    return RegistrationService()


@router.get("", response_model=List[RegistrationOut])
def get_registrations(
    *,
    db: Session = Depends(get_db),
    service: RegistrationService = Depends(get_registration_service),
    commons: CommonQueryParams = Depends(),
    school_year_id: Optional[int] = None,
    grade_id: Optional[int] = None,
    regi_no: Optional[str] = None,
):
    return service.get_registrations(
        db,
        skip=commons.skip,
        limit=commons.limit,
        school_year_id=school_year_id,
        grade_id=grade_id,
        regi_no=regi_no,
    )


@router.get("/{registration_id}", response_model=RegistrationOut)
def get_registration(
    *,
    db: Session = Depends(get_db),
    service: RegistrationService = Depends(get_registration_service),
    registration_id: int,
):
    return service.get_registration(db, registration_id=registration_id)


@router.post("", response_model=RegistrationOut, status_code=status.HTTP_201_CREATED)
def create_registration(
    *,
    db: Session = Depends(get_db),
    service: RegistrationService = Depends(get_registration_service),
    registration_in: RegistrationIn,
):
    return service.create_registration(db, registration_in=registration_in)
