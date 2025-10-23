"""Dependency injection for the GoldenCity Memo API.

This module provides dependency injection functions for better testability
and separation of concerns.
"""

from .storage import NoteStorage

# Global storage instance (for simplicity in this demo)
# In production, this would be a database connection pool
_storage_instance = None


def get_storage() -> NoteStorage:
    """Get storage instance using dependency injection pattern.
    
    Returns:
        NoteStorage instance
    """
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = NoteStorage()
    return _storage_instance


def reset_storage() -> None:
    """Reset storage instance (useful for testing).
    
    This function allows tests to start with a clean storage state.
    """
    global _storage_instance
    _storage_instance = None
