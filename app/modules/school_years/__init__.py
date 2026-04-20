"""School years module package."""

from app.modules.school_years.router import router
from app.modules.school_years.service import SchoolYearService

__all__ = ["router", "SchoolYearService"]
