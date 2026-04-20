"""School year module schemas.

This module re-exports existing school year schemas to support gradual migration.
"""

from app.schemas.school_year import SchoolYearCreate, SchoolYearInDB, SchoolYearUpdate

__all__ = ["SchoolYearCreate", "SchoolYearInDB", "SchoolYearUpdate"]
