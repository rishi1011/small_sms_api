"""Nationality module schemas.

This module re-exports existing nationality schemas to support gradual migration.
"""

from app.schemas.nationality import NationalityCreate, NationalityInDB, NationalityUpdate

__all__ = ["NationalityCreate", "NationalityInDB", "NationalityUpdate"]
