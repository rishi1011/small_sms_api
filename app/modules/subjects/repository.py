"""Repository layer for subject data access."""

from sqlalchemy.orm import Session

from app import crud
from app.modules.subjects.schemas import SubjectCreate, SubjectUpdate


class SubjectRepository:
    def get_multi(self, db: Session, skip: int = 0, limit: int = 20):
        return crud.subject.get_multi(db, skip=skip, limit=limit)

    def get(self, db: Session, subject_id: int):
        return crud.subject.get(db, id=subject_id)

    def get_by_name(self, db: Session, name: str):
        return crud.subject.get_by_name(db, name=name)

    def create(self, db: Session, subject_in: SubjectCreate):
        return crud.subject.create(db, obj_in=subject_in)

    def update(self, db: Session, db_obj, subject_in: SubjectUpdate):
        return crud.subject.update(db, db_obj=db_obj, obj_in=subject_in)

    def remove(self, db: Session, subject_id: int):
        return crud.subject.remove(db, id=subject_id)
