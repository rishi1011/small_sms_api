"""Service layer for nationality business logic."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.nationalities.repository import NationalityRepository
from app.modules.nationalities.schemas import NationalityCreate, NationalityUpdate


class NationalityService:
    def __init__(self, repository: NationalityRepository | None = None):
        self.repository = repository or NationalityRepository()

    def get_nationalities(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repository.get_multi(db, skip=skip, limit=limit)

    def get_nationality(self, db: Session, nationality_id: int):
        nationality = self.repository.get(db, nationality_id)
        if not nationality:
            raise HTTPException(status_code=404, detail="Nationality not found")
        return nationality

    def create_nationality(self, db: Session, nationality_in: NationalityCreate):
        nationality = self.repository.get_by_name(
            db, nationality_in.masculine_form, nationality_in.feminine_form
        )
        if nationality:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Redundant data."
            )
        return self.repository.create(db, nationality_in=nationality_in)

    def update_nationality(
        self, db: Session, nationality_id: int, nationality_in: NationalityUpdate
    ):
        nationality = self.repository.get(db, nationality_id)
        if not nationality:
            raise HTTPException(status_code=404, detail="Nationality not found")

        existing_nationality = self.repository.get_by_name(
            db, nationality_in.masculine_form, nationality_in.feminine_form
        )
        if existing_nationality and existing_nationality.id != nationality_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Redundant data.",
            )
        return self.repository.update(db, db_obj=nationality, nationality_in=nationality_in)

    def delete_nationality(self, db: Session, nationality_id: int):
        nationality = self.repository.get(db, nationality_id)
        if not nationality:
            raise HTTPException(status_code=404, detail="Nationality not found")
        if nationality.students:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There are students data depends on this nationality.",
            )
        self.repository.remove(db, nationality_id=nationality_id)
