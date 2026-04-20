"""Registrations module package."""

from app.modules.registrations.router import router
from app.modules.registrations.service import RegistrationService

__all__ = ["router", "RegistrationService"]
