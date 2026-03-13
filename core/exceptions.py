"""
Cel-Logic Pro — Custom Exception Hierarchy
Controlled error handling. Operators catch CelLogicError subtypes.
"""


class CelLogicError(Exception):
    """Base exception for all Cel-Logic errors."""
    pass


class EngineMismatchError(CelLogicError):
    """Raised when the render engine is not compatible."""
    pass


class MissingObjectError(CelLogicError):
    """Raised when an expected object is not found."""
    pass


class MaterialError(CelLogicError):
    """Raised when material creation or modification fails."""
    pass


class ModifierError(CelLogicError):
    """Raised when modifier operations fail."""
    pass


class DriverError(CelLogicError):
    """Raised when driver creation or removal fails."""
    pass


class PropertyError(CelLogicError):
    """Raised when property access is invalid."""
    pass


class MigrationError(CelLogicError):
    """Raised when data migration fails."""
    pass
