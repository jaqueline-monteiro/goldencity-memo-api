"""Tests for dependency injection module.

This module tests the dependency injection functionality
to ensure proper storage management and isolation.
"""

try:
    from app.dependencies import get_storage, reset_storage
    from app.storage import NoteStorage
except ImportError:
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.dependencies import get_storage, reset_storage
    from app.storage import NoteStorage


class TestDependencies:
    """Test cases for dependency injection."""

    def test_get_storage_returns_instance(self):
        """Test that get_storage returns a NoteStorage instance."""
        storage = get_storage()
        assert isinstance(storage, NoteStorage)

    def test_get_storage_singleton_behavior(self):
        """Test that get_storage returns the same instance on multiple calls."""
        storage1 = get_storage()
        storage2 = get_storage()
        assert storage1 is storage2

    def test_reset_storage_creates_new_instance(self):
        """Test that reset_storage allows getting a fresh instance."""
        storage1 = get_storage()
        reset_storage()
        storage2 = get_storage()
        assert storage1 is not storage2

    def test_storage_isolation_after_reset(self):
        """Test that storage data is isolated after reset."""
        from app.models import NoteCreate

        # Get storage and add a note
        storage1 = get_storage()
        note_data = NoteCreate(title="Test Note", content="Test content")
        storage1.create(note_data)
        assert len(storage1.get_all()) == 1

        # Reset and get new storage
        reset_storage()
        storage2 = get_storage()
        assert len(storage2.get_all()) == 0
        assert storage1 is not storage2
