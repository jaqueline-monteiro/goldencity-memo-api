"""API routes for the GoldenCity Memo API.

This module defines all the REST endpoints for note management operations.
"""

import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends

from .dependencies import get_storage
from .models import Note, NoteCreate, NoteUpdate
from .storage import NoteStorage

logger = logging.getLogger(__name__)

router = APIRouter(tags=["notes"])


@router.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(
        note: NoteCreate,
        storage: NoteStorage = Depends(get_storage)
) -> Note:
    """Create a new note.
    
    Args:
        note: Note creation data
        storage: Storage dependency
        
    Returns:
        Created note with generated ID and timestamps
        
    Raises:
        HTTPException: 422 if validation fails, 500 for server errors
    """
    logger.info("Creating note with title: %s", note.title)
    try:
        created_note = storage.create(note)
        logger.info("Note created successfully with ID: %s", created_note.id)
        return created_note
    except Exception as e:
        logger.error("Error creating note: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create note"
        ) from e


@router.get("/notes", response_model=List[Note])
def get_notes(storage: NoteStorage = Depends(get_storage)) -> List[Note]:
    """Get all notes.
    
    Args:
        storage: Storage dependency
    
    Returns:
        List of all notes sorted by creation date (newest first)
    """
    logger.info("Retrieving all notes")
    try:
        notes = storage.get_all()
        logger.info("Retrieved %d notes successfully", len(notes))
        return notes
    except Exception as e:
        logger.error("Error retrieving notes: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notes"
        ) from e


@router.get("/notes/{note_id}", response_model=Note)
def get_note(
        note_id: UUID,
        storage: NoteStorage = Depends(get_storage)
) -> Note:
    """Get a specific note by ID.
    
    Args:
        note_id: UUID of the note to retrieve
        storage: Storage dependency
        
    Returns:
        The requested note
        
    Raises:
        HTTPException: 404 if note not found, 500 for server errors
    """
    logger.info("Retrieving note with ID: %s", note_id)
    try:
        note = storage.get_by_id(note_id)
        if not note:
            logger.warning("Note not found with ID: %s", note_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        logger.info("Note retrieved successfully with ID: %s", note_id)
        return note
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error retrieving note %s: %s", note_id, str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve note"
        ) from e


@router.put("/notes/{note_id}", response_model=Note)
def update_note(
        note_id: UUID,
        note_update: NoteUpdate,
        storage: NoteStorage = Depends(get_storage)
) -> Note:
    """Update an existing note.
    
    Args:
        note_id: UUID of the note to update
        note_update: Partial update data
        storage: Storage dependency
        
    Returns:
        Updated note
        
    Raises:
        HTTPException: 404 if note not found, 422 if validation fails, 500 for server errors
    """
    logger.info("Updating note with ID: %s", note_id)
    try:
        note = storage.update(note_id, note_update)
        if not note:
            logger.warning("Cannot update - note not found with ID: %s", note_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        logger.info("Note updated successfully with ID: %s", note_id)
        return note
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating note %s: %s", note_id, str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update note"
        ) from e


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
        note_id: UUID,
        storage: NoteStorage = Depends(get_storage)
) -> None:
    """Delete a note by ID.
    
    Args:
        note_id: UUID of the note to delete
        storage: Storage dependency
        
    Raises:
        HTTPException: 404 if note not found, 500 for server errors
    """
    logger.info("Deleting note with ID: %s", note_id)
    try:
        if not storage.delete(note_id):
            logger.warning("Cannot delete - note not found with ID: %s", note_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        logger.info("Note deleted successfully with ID: %s", note_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting note %s: %s", note_id, str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete note"
        ) from e
