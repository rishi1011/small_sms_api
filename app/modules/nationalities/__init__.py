"""Nationalities module package."""

from app.modules.nationalities.router import router
from app.modules.nationalities.service import NationalityService

__all__ = ["router", "NationalityService"]
