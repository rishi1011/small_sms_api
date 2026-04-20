"""Service layer for subject business logic."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.subjects.repository import SubjectRepository
from app.modules.subjects.schemas import SubjectCreate, SubjectUpdate


class SubjectService:
    def __init__(self, repository: SubjectRepository | None = None):
        self.repository = repository or SubjectRepository()

    def get_subjects(self, db: Session, skip: int = 0, limit: int = 20):
        return self.repository.get_multi(db, skip=skip, limit=limit)

    def get_subject(self, db: Session, subject_id: int):
        subject = self.repository.get(db, subject_id)
        if not subject:
            raise HTTPException(
                status_code=404, detail=f"Subject with id {subject_id} does not exist"
            )
        return subject

    def create_subject(self, db: Session, subject_in: SubjectCreate):
        subject = self.repository.get_by_name(db, name=subject_in.name)
        if subject:
            raise HTTPException(
                status_code=409, detail="A subject with this name already exists"
            )
        return self.repository.create(db, subject_in=subject_in)

    def update_subject(self, db: Session, subject_id: int, subject_in: SubjectUpdate):
        subject = self.repository.get(db, subject_id)
        if not subject:
            raise HTTPException(
                status_code=404, detail=f"Subject with id {subject_id} does not exist"
            )
        return self.repository.update(db, db_obj=subject, subject_in=subject_in)

    def delete_subject(self, db: Session, subject_id: int):
        subject = self.repository.get(db, subject_id)
        if not subject:
            raise HTTPException(
                status_code=404, detail=f"Subject with id {subject_id} does not exist"
            )
        self.repository.remove(db, subject_id=subject_id)
