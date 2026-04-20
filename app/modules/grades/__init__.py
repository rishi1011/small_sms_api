"""Grades module package."""

from app.modules.grades.router import router
from app.modules.grades.service import GradeService

__all__ = ["router", "GradeService"]
