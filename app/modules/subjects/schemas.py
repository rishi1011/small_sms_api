"""Subject module schemas.

This module re-exports existing subject schemas to support gradual migration.
"""

from app.schemas.subject import SubjectCreate, SubjectInDB, SubjectUpdate

__all__ = ["SubjectCreate", "SubjectInDB", "SubjectUpdate"]
