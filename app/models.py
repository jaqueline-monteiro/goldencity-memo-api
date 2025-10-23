"""Pydantic models for the GoldenCity Memo API.

This module defines the data models used throughout the API for validation,
serialization, and documentation.
"""

from datetime import datetime, UTC
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base model for note data validation.
    
    Contains the common fields shared between create and response models.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Note title")
    content: str = Field(..., min_length=1, description="Note content")


class NoteCreate(NoteBase):
    """Model for creating a new note.
    
    Inherits all validation rules from NoteBase.
    """
    pass


class NoteUpdate(BaseModel):
    """Model for updating an existing note.
    
    All fields are optional to support partial updates.
    """
    title: str | None = Field(None, min_length=1, max_length=200, description="Updated note title")
    content: str | None = Field(None, min_length=1, description="Updated note content")


class Note(NoteBase):
    """Complete note model with metadata.
    
    Includes auto-generated ID and timestamps.
    """
    id: UUID = Field(default_factory=uuid4, description="Unique note identifier")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Creation timestamp")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Last update timestamp")

    model_config = {"from_attributes": True}
