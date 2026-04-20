"""Repository layer for nationality data access."""

from sqlalchemy.orm import Session

from app import crud
from app.modules.nationalities.schemas import NationalityCreate, NationalityUpdate


class NationalityRepository:
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return crud.nationality.get_multi(db, skip=skip, limit=limit)

    def get(self, db: Session, nationality_id: int):
        return crud.nationality.get(db, nationality_id)

    def get_by_name(self, db: Session, masculine_form: str, feminine_form: str):
        return crud.nationality.get_by_name(db, masculine_form, feminine_form)

    def create(self, db: Session, nationality_in: NationalityCreate):
        return crud.nationality.create(db, obj_in=nationality_in)

    def update(self, db: Session, db_obj, nationality_in: NationalityUpdate):
        return crud.nationality.update(db, db_obj=db_obj, obj_in=nationality_in)

    def remove(self, db: Session, nationality_id: int):
        return crud.nationality.remove(db, id=nationality_id)
