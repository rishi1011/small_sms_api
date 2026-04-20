"""Student module schemas.

This file re-exports existing schemas to support gradual migration
from `app.schemas.student` into the module-based architecture.
"""

from app.schemas.student import Base, StudentCreate, StudentInDB, StudentUpdate

__all__ = ["Base", "StudentCreate", "StudentUpdate", "StudentInDB"]
