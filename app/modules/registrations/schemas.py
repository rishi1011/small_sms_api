"""Registration module schemas.

This module re-exports existing registration schemas to support gradual migration.
"""

from app.schemas.registration import (
    RegistrationCreate,
    RegistrationIn,
    RegistrationOut,
    RegistrationUpdate,
)

__all__ = ["RegistrationCreate", "RegistrationIn", "RegistrationOut", "RegistrationUpdate"]
