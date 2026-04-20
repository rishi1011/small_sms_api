"""Subjects module package."""

from app.modules.subjects.router import router
from app.modules.subjects.service import SubjectService

__all__ = ["router", "SubjectService"]
