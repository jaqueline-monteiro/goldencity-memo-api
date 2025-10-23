"""Comprehensive test suite for the GoldenCity Memo API.

This module contains unit tests, integration tests, and error scenario tests
for all API endpoints and functionality.
"""

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

try:
    from app.main import app
    from app.dependencies import get_storage, reset_storage
    from app.storage import NoteStorage
    from app.models import Note
except ImportError:
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.main import app
    from app.dependencies import get_storage, reset_storage
    from app.storage import NoteStorage
    from app.models import Note


@pytest.fixture
def client():
    """Create test client with shared storage for each test."""
    test_storage = NoteStorage()

    def get_test_storage():
        return test_storage

    app.dependency_overrides[get_storage] = get_test_storage
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def storage():
    """Create fresh storage instance for direct testing."""
    return NoteStorage()


class TestHealthCheck:
    """Test cases for health check endpoint."""

    def test_root_endpoint(self, client):
        """Test the root health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "GoldenCity Memo API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "healthy"


class TestNoteCreation:
    """Test cases for note creation."""

    def test_create_note_success(self, client):
        """Test successful note creation."""
        note_data = {"title": "Test Note", "content": "Test content"}
        response = client.post("/notes", json=note_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Note"
        assert data["content"] == "Test content"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_note_empty_title(self, client):
        """Test note creation with empty title."""
        note_data = {"title": "", "content": "Test content"}
        response = client.post("/notes", json=note_data)
        assert response.status_code == 422

    def test_create_note_empty_content(self, client):
        """Test note creation with empty content."""
        note_data = {"title": "Test Title", "content": ""}
        response = client.post("/notes", json=note_data)
        assert response.status_code == 422

    def test_create_note_missing_fields(self, client):
        """Test note creation with missing required fields."""
        response = client.post("/notes", json={})
        assert response.status_code == 422

    def test_create_note_title_too_long(self, client):
        """Test note creation with title exceeding max length."""
        note_data = {
            "title": "x" * 201,  # Exceeds 200 char limit
            "content": "Test content"
        }
        response = client.post("/notes", json=note_data)
        assert response.status_code == 422


class TestNoteRetrieval:
    """Test cases for note retrieval."""

    def test_get_notes_empty(self, client):
        """Test getting notes when storage is empty."""
        response = client.get("/notes")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_notes_with_data(self, client):
        """Test getting notes when storage has data."""
        # Create a note first
        note_data = {"title": "Test Note", "content": "Test content"}
        client.post("/notes", json=note_data)

        response = client.get("/notes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1

    def test_get_note_by_id_success(self, client):
        """Test successful note retrieval by ID."""
        # Create a note first
        note_data = {"title": "Test Note", "content": "Test content"}
        create_response = client.post("/notes", json=note_data)
        note_id = create_response.json()["id"]

        # Get the note
        response = client.get(f"/notes/{note_id}")
        assert response.status_code == 200
        assert response.json()["id"] == note_id

    def test_get_note_by_id_not_found(self, client):
        """Test note retrieval with non-existent ID."""
        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        response = client.get(f"/notes/{fake_id}")
        assert response.status_code == 404
        assert "Note not found" in response.json()["detail"]

    def test_get_note_invalid_uuid(self, client):
        """Test note retrieval with invalid UUID format."""
        response = client.get("/notes/invalid-uuid")
        assert response.status_code == 422


class TestNoteUpdate:
    """Test cases for note updates."""

    def test_update_note_success(self, client):
        """Test successful note update."""
        # Create a note first
        note_data = {"title": "Original Title", "content": "Original content"}
        create_response = client.post("/notes", json=note_data)
        note_id = create_response.json()["id"]

        # Update the note
        update_data = {"title": "Updated Title", "content": "Updated content"}
        response = client.put(f"/notes/{note_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"
        assert data["id"] == note_id

    def test_update_note_partial(self, client):
        """Test partial note update (only title)."""
        # Create a note first
        note_data = {"title": "Original Title", "content": "Original content"}
        create_response = client.post("/notes", json=note_data)
        note_id = create_response.json()["id"]

        # Update only the title
        update_data = {"title": "Updated Title"}
        response = client.put(f"/notes/{note_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Original content"  # Should remain unchanged

    def test_update_note_not_found(self, client):
        """Test updating non-existent note."""
        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        update_data = {"title": "Updated Title"}
        response = client.put(f"/notes/{fake_id}", json=update_data)
        assert response.status_code == 404

    def test_update_note_empty_fields(self, client):
        """Test updating note with empty fields."""
        # Create a note first
        note_data = {"title": "Original Title", "content": "Original content"}
        create_response = client.post("/notes", json=note_data)
        note_id = create_response.json()["id"]

        # Try to update with empty title
        update_data = {"title": ""}
        response = client.put(f"/notes/{note_id}", json=update_data)
        assert response.status_code == 422


class TestNoteDeletion:
    """Test cases for note deletion."""

    def test_delete_note_success(self, client):
        """Test successful note deletion."""
        # Create a note first
        note_data = {"title": "To Delete", "content": "Delete me"}
        create_response = client.post("/notes", json=note_data)
        note_id = create_response.json()["id"]

        # Delete the note
        response = client.delete(f"/notes/{note_id}")
        assert response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"/notes/{note_id}")
        assert get_response.status_code == 404

    def test_delete_note_not_found(self, client):
        """Test deleting non-existent note."""
        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        response = client.delete(f"/notes/{fake_id}")
        assert response.status_code == 404


class TestIntegrationMocked:
    """Integration tests with mocked dependencies."""

    def test_create_note_storage_error(self, client):
        """Test note creation when storage fails."""

        def get_failing_storage():
            mock_storage = MagicMock()
            mock_storage.create.side_effect = Exception("Storage error")
            return mock_storage

        app.dependency_overrides[get_storage] = get_failing_storage

        note_data = {"title": "Test Note", "content": "Test content"}
        response = client.post("/notes", json=note_data)
        assert response.status_code == 500

        app.dependency_overrides.clear()

    def test_get_notes_storage_error(self, client):
        """Test getting notes when storage fails."""

        def get_failing_storage():
            mock_storage = MagicMock()
            mock_storage.get_all.side_effect = Exception("Storage error")
            return mock_storage

        app.dependency_overrides[get_storage] = get_failing_storage

        response = client.get("/notes")
        assert response.status_code == 500

        app.dependency_overrides.clear()

    def test_get_note_storage_error(self, client):
        """Test getting note by ID when storage fails."""

        def get_failing_storage():
            mock_storage = MagicMock()
            mock_storage.get_by_id.side_effect = Exception("Storage error")
            return mock_storage

        app.dependency_overrides[get_storage] = get_failing_storage

        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        response = client.get(f"/notes/{fake_id}")
        assert response.status_code == 500

        app.dependency_overrides.clear()

    def test_update_note_storage_error(self, client):
        """Test updating note when storage fails."""

        def get_failing_storage():
            mock_storage = MagicMock()
            mock_storage.update.side_effect = Exception("Storage error")
            return mock_storage

        app.dependency_overrides[get_storage] = get_failing_storage

        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        update_data = {"title": "Updated Title"}
        response = client.put(f"/notes/{fake_id}", json=update_data)
        assert response.status_code == 500

        app.dependency_overrides.clear()

    def test_delete_note_storage_error(self, client):
        """Test deleting note when storage fails."""

        def get_failing_storage():
            mock_storage = MagicMock()
            mock_storage.delete.side_effect = Exception("Storage error")
            return mock_storage

        app.dependency_overrides[get_storage] = get_failing_storage

        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        response = client.delete(f"/notes/{fake_id}")
        assert response.status_code == 500

        app.dependency_overrides.clear()


class TestDataFlow:
    """End-to-end data flow tests."""

    def test_complete_crud_flow(self, client):
        """Test complete CRUD operations flow."""
        # 1. Create a note
        note_data = {"title": "CRUD Test", "content": "Testing CRUD operations"}
        create_response = client.post("/notes", json=note_data)
        assert create_response.status_code == 201
        note_id = create_response.json()["id"]

        # 2. Read the note
        get_response = client.get(f"/notes/{note_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "CRUD Test"

        # 3. Update the note
        update_data = {"title": "Updated CRUD Test"}
        update_response = client.put(f"/notes/{note_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated CRUD Test"

        # 4. Delete the note
        delete_response = client.delete(f"/notes/{note_id}")
        assert delete_response.status_code == 204

        # 5. Verify deletion
        final_get_response = client.get(f"/notes/{note_id}")
        assert final_get_response.status_code == 404

    def test_multiple_notes_ordering(self, client):
        """Test that multiple notes are returned in correct order."""
        import time

        # Create multiple notes with slight delays
        notes_data = [
            {"title": "First Note", "content": "First content"},
            {"title": "Second Note", "content": "Second content"},
            {"title": "Third Note", "content": "Third content"}
        ]

        created_ids = []
        for note_data in notes_data:
            response = client.post("/notes", json=note_data)
            created_ids.append(response.json()["id"])
            time.sleep(0.001)  # Ensure different timestamps

        # Get all notes
        response = client.get("/notes")
        assert response.status_code == 200
        notes = response.json()

        # Should be ordered by creation time (newest first)
        assert len(notes) == 3
        assert notes[0]["title"] == "Third Note"  # Most recent
        assert notes[2]["title"] == "First Note"  # Oldest
