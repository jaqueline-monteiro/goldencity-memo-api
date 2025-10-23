"""Unit tests for the storage layer.

This module tests the storage layer in isolation to ensure
proper data handling and business logic.
"""

import time
from uuid import uuid4

import pytest

try:
    from app.storage import NoteStorage
    from app.models import NoteCreate, NoteUpdate
except ImportError:
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.storage import NoteStorage
    from app.models import NoteCreate, NoteUpdate


class TestNoteStorage:
    """Test cases for NoteStorage class."""

    @pytest.fixture
    def storage(self):
        """Set up fresh storage for each test."""
        return NoteStorage()

    def test_create_note(self, storage):
        """Test note creation in storage."""
        note_data = NoteCreate(title="Test Note", content="Test content")
        note = storage.create(note_data)

        assert note.title == "Test Note"
        assert note.content == "Test content"
        assert note.id is not None
        assert note.created_at is not None
        assert note.updated_at is not None
        assert len(storage._notes) == 1

    def test_get_all_empty(self, storage):
        """Test getting all notes from empty storage."""
        notes = storage.get_all()
        assert notes == []

    def test_get_all_with_notes(self, storage):
        """Test getting all notes with data."""
        # Create multiple notes with slight delay
        created_notes = []
        for i in range(3):
            note_data = NoteCreate(title=f"Note {i}", content=f"Content {i}")
            note = storage.create(note_data)
            created_notes.append(note)
            time.sleep(0.001)  # Ensure different timestamps

        notes = storage.get_all()
        assert len(notes) == 3
        # Should be sorted by creation time (newest first)
        assert notes[0].title == "Note 2"
        assert notes[2].title == "Note 0"

    def test_get_by_id_existing(self, storage):
        """Test getting note by existing ID."""
        note_data = NoteCreate(title="Test Note", content="Test content")
        created_note = storage.create(note_data)

        retrieved_note = storage.get_by_id(created_note.id)
        assert retrieved_note is not None
        assert retrieved_note.id == created_note.id
        assert retrieved_note.title == "Test Note"

    def test_get_by_id_non_existing(self, storage):
        """Test getting note by non-existing ID."""
        fake_id = uuid4()
        note = storage.get_by_id(fake_id)
        assert note is None

    def test_update_existing_note(self, storage):
        """Test updating an existing note."""
        # Create a note
        note_data = NoteCreate(title="Original Title", content="Original content")
        created_note = storage.create(note_data)
        original_updated_at = created_note.updated_at

        # Small delay to ensure different timestamp
        time.sleep(0.001)

        # Update the note
        update_data = NoteUpdate(title="Updated Title", content="Updated content")
        updated_note = storage.update(created_note.id, update_data)

        assert updated_note is not None
        assert updated_note.title == "Updated Title"
        assert updated_note.content == "Updated content"
        assert updated_note.updated_at >= original_updated_at

    def test_update_partial(self, storage):
        """Test partial update of a note."""
        # Create a note
        note_data = NoteCreate(title="Original Title", content="Original content")
        created_note = storage.create(note_data)

        # Update only title
        update_data = NoteUpdate(title="Updated Title")
        updated_note = storage.update(created_note.id, update_data)

        assert updated_note is not None
        assert updated_note.title == "Updated Title"
        assert updated_note.content == "Original content"  # Should remain unchanged

    def test_update_non_existing_note(self, storage):
        """Test updating a non-existing note."""
        fake_id = uuid4()
        update_data = NoteUpdate(title="Updated Title")
        result = storage.update(fake_id, update_data)
        assert result is None

    def test_delete_existing_note(self, storage):
        """Test deleting an existing note."""
        # Create a note
        note_data = NoteCreate(title="To Delete", content="Delete me")
        created_note = storage.create(note_data)

        # Delete the note
        result = storage.delete(created_note.id)
        assert result is True
        assert len(storage._notes) == 0

        # Verify it's gone
        retrieved_note = storage.get_by_id(created_note.id)
        assert retrieved_note is None

    def test_delete_non_existing_note(self, storage):
        """Test deleting a non-existing note."""
        fake_id = uuid4()
        result = storage.delete(fake_id)
        assert result is False

    def test_clear_storage(self, storage):
        """Test clearing all notes from storage."""
        # Create some notes
        for i in range(3):
            note_data = NoteCreate(title=f"Note {i}", content=f"Content {i}")
            storage.create(note_data)

        assert len(storage._notes) == 3

        # Clear storage
        storage.clear()
        assert len(storage._notes) == 0
        assert storage.get_all() == []

    def test_timestamp_consistency(self, storage):
        """Test that timestamps are properly set and updated."""
        # Create a note
        note_data = NoteCreate(title="Timestamp Test", content="Testing timestamps")
        created_note = storage.create(note_data)

        # Check that created_at and updated_at are initially the same
        assert created_note.created_at == created_note.updated_at

        # Wait a bit and update
        time.sleep(0.001)
        update_data = NoteUpdate(title="Updated Title")
        updated_note = storage.update(created_note.id, update_data)

        # Check that updated_at changed but created_at didn't
        assert updated_note.created_at == created_note.created_at
        assert updated_note.updated_at >= created_note.updated_at
