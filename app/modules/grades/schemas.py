"""Grade module schemas.

This module re-exports existing grade schemas to support gradual migration.
"""

from app.schemas.grade import GradeCreate, GradeInDB, GradeUpdate
from app.schemas.grade_subject import (
    GradeSubjectCreate,
    GradeSubjectOut,
    GradeSubjectUpdate,
    GradeSubjectsOut,
)

__all__ = [
    "GradeCreate",
    "GradeInDB",
    "GradeUpdate",
    "GradeSubjectCreate",
    "GradeSubjectOut",
    "GradeSubjectUpdate",
    "GradeSubjectsOut",
]
