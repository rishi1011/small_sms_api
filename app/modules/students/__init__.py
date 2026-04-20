"""Students module package."""

from app.modules.students.router import router
from app.modules.students.service import StudentService

__all__ = ["router", "StudentService"]
