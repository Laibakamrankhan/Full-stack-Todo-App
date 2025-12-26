"""Tests for the Task model."""

import pytest
from datetime import datetime
from src.models.task import Task
from src.models.enums import TaskStatus


class TestTask:
    """Test cases for the Task model."""

    def test_task_creation_with_required_fields(self):
        """Test creating a task with required fields only."""
        task = Task(id="test-id", title="Test Task")

        assert task.id == "test-id"
        assert task.title == "Test Task"
        assert task.description is None
        assert task.status == TaskStatus.PENDING
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields."""
        created_time = datetime(2023, 1, 1, 12, 0, 0)
        task = Task(
            id="test-id",
            title="Test Task",
            description="Test Description",
            status=TaskStatus.COMPLETED,
            created_at=created_time,
            updated_at=created_time
        )

        assert task.id == "test-id"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == TaskStatus.COMPLETED
        assert task.created_at == created_time
        assert task.updated_at == created_time

    def test_task_creation_sets_default_datetime(self):
        """Test that task creation sets default datetime values."""
        task = Task(id="test-id", title="Test Task")

        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)
        assert task.created_at == task.updated_at

    def test_task_update_method(self):
        """Test updating task fields."""
        task = Task(id="test-id", title="Original Title", description="Original Description")
        original_created = task.created_at

        task.update(title="New Title", description="New Description")

        assert task.title == "New Title"
        assert task.description == "New Description"
        assert task.created_at == original_created  # Should not change
        assert task.updated_at > original_created  # Should be updated

    def test_task_update_partial_fields(self):
        """Test updating only some fields."""
        task = Task(id="test-id", title="Original Title", description="Original Description")

        # Update only title
        task.update(title="New Title")
        assert task.title == "New Title"
        assert task.description == "Original Description"  # Should remain unchanged

        # Update only description
        task.update(description="Updated Description")
        assert task.title == "New Title"  # Should remain unchanged
        assert task.description == "Updated Description"

    def test_task_update_none_values(self):
        """Test updating with None values."""
        task = Task(id="test-id", title="Test Title", description="Test Description")

        # Update with None should not change the field
        task.update(title=None, description=None)
        assert task.title == "Test Title"
        assert task.description == "Test Description"

    def test_task_toggle_status_pending_to_completed(self):
        """Test toggling status from pending to completed."""
        task = Task(id="test-id", title="Test Task", status=TaskStatus.PENDING)
        original_created = task.created_at

        task.toggle_status()

        assert task.status == TaskStatus.COMPLETED
        assert task.created_at == original_created  # Should not change
        assert task.updated_at > original_created  # Should be updated

    def test_task_toggle_status_completed_to_pending(self):
        """Test toggling status from completed to pending."""
        task = Task(id="test-id", title="Test Task", status=TaskStatus.COMPLETED)
        original_created = task.created_at

        task.toggle_status()

        assert task.status == TaskStatus.PENDING
        assert task.created_at == original_created  # Should not change
        assert task.updated_at > original_created  # Should be updated