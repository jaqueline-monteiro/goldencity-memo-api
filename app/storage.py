"""In-memory storage layer for the GoldenCity Memo API.

This module provides a simple in-memory storage implementation for notes.
In production, this would be replaced with a proper database layer.
"""

import logging
from datetime import datetime, UTC
from typing import List, Optional
from uuid import UUID

from .models import Note, NoteCreate, NoteUpdate

logger = logging.getLogger(__name__)


class NoteStorage:
    """In-memory storage for notes with CRUD operations."""

    def __init__(self):
        """Initialize empty storage."""
        self._notes: List[Note] = []
        logger.info("NoteStorage initialized")

    def create(self, note_data: NoteCreate) -> Note:
        """Create a new note.
        
        Args:
            note_data: Note creation data
            
        Returns:
            Created note with generated ID and timestamps
        """
        note = Note(**note_data.model_dump())
        self._notes.append(note)
        logger.info("Note created with ID: %s", note.id)
        return note

    def get_all(self) -> List[Note]:
        """Get all notes sorted by creation date (newest first).
        
        Returns:
            List of all notes
        """
        notes = sorted(self._notes, key=lambda x: x.created_at, reverse=True)
        logger.info("Retrieved %d notes", len(notes))
        return notes

    def get_by_id(self, note_id: UUID) -> Optional[Note]:
        """Get a note by its ID.
        
        Args:
            note_id: UUID of the note to retrieve
            
        Returns:
            Note if found, None otherwise
        """
        note = next((note for note in self._notes if note.id == note_id), None)
        if note:
            logger.info("Note found with ID: %s", note_id)
        else:
            logger.warning("Note not found with ID: %s", note_id)
        return note

    def update(self, note_id: UUID, note_data: NoteUpdate) -> Optional[Note]:
        """Update an existing note.
        
        Args:
            note_id: UUID of the note to update
            note_data: Update data (partial)
            
        Returns:
            Updated note if found, None otherwise
        """
        note = self.get_by_id(note_id)
        if not note:
            logger.warning("Cannot update - note not found with ID: %s", note_id)
            return None

        # Apply partial updates
        update_data = note_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(note, field, value)

        # Update timestamp
        note.updated_at = datetime.now(UTC)
        logger.info("Note updated with ID: %s", note_id)
        return note

    def delete(self, note_id: UUID) -> bool:
        """Delete a note by its ID.
        
        Args:
            note_id: UUID of the note to delete
            
        Returns:
            True if deleted, False if not found
        """
        note = self.get_by_id(note_id)
        if note:
            self._notes.remove(note)
            logger.info("Note deleted with ID: %s", note_id)
            return True
        logger.warning("Cannot delete - note not found with ID: %s", note_id)
        return False

    def clear(self) -> None:
        """Clear all notes from storage.
        
        Useful for testing and cleanup operations.
        """
        count = len(self._notes)
        self._notes.clear()
        logger.info("Cleared %d notes from storage", count)
