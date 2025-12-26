"""Tests for the task service."""

import pytest
from unittest.mock import Mock
from src.services.task_service import TaskService
from src.models.task import Task
from src.models.enums import TaskStatus
from src.repositories.base import TaskRepository


class TestTaskService:
    """Test cases for the TaskService."""

    def setup_method(self):
        """Set up a mock repository and service for each test."""
        self.mock_repository = Mock(spec=TaskRepository)
        self.service = TaskService(self.mock_repository)

    def test_add_task_success(self):
        """Test adding a task successfully."""
        self.mock_repository.add_task.return_value = Task(id="new-id", title="New Task")

        result = self.service.add_task("New Task", "Description")

        assert result.id == "new-id"
        assert result.title == "New Task"
        self.mock_repository.add_task.assert_called_once()

    def test_add_task_empty_title_raises_error(self):
        """Test that adding a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            self.service.add_task("")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            self.service.add_task("   ")  # Only whitespace

        # Verify repository method was not called
        self.mock_repository.add_task.assert_not_called()

    def test_add_task_strips_whitespace(self):
        """Test that task title and description are stripped of whitespace."""
        self.mock_repository.add_task.return_value = Task(id="new-id", title="New Task")

        result = self.service.add_task("  New Task  ", "  Description  ")

        # Check that add_task was called with stripped values
        self.mock_repository.add_task.assert_called_once()
        called_task = self.mock_repository.add_task.call_args[0][0]
        assert called_task.title == "New Task"
        assert called_task.description == "Description"

    def test_list_tasks(self):
        """Test listing all tasks."""
        expected_tasks = [Task(id="id1", title="Task 1"), Task(id="id2", title="Task 2")]
        self.mock_repository.get_all_tasks.return_value = expected_tasks

        result = self.service.list_tasks()

        assert result == expected_tasks
        self.mock_repository.get_all_tasks.assert_called_once()

    def test_get_task(self):
        """Test getting a specific task."""
        expected_task = Task(id="test-id", title="Test Task")
        self.mock_repository.get_task_by_id.return_value = expected_task

        result = self.service.get_task("test-id")

        assert result == expected_task
        self.mock_repository.get_task_by_id.assert_called_once_with("test-id")

    def test_update_task_success(self):
        """Test updating a task successfully."""
        existing_task = Task(id="test-id", title="Old Title", description="Old Description")
        updated_task = Task(id="test-id", title="New Title", description="New Description")

        self.mock_repository.get_task_by_id.return_value = existing_task
        self.mock_repository.update_task.return_value = updated_task

        result = self.service.update_task("test-id", "New Title", "New Description")

        assert result == updated_task
        self.mock_repository.update_task.assert_called_once_with("test-id", "New Title", "New Description")

    def test_update_task_empty_title_raises_error(self):
        """Test that updating a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            self.service.update_task("test-id", "")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            self.service.update_task("test-id", "   ")  # Only whitespace

        # Verify repository method was not called for update
        self.mock_repository.update_task.assert_not_called()

    def test_update_task_strips_whitespace(self):
        """Test that updated task title and description are stripped of whitespace."""
        existing_task = Task(id="test-id", title="Old Title")
        self.mock_repository.get_task_by_id.return_value = existing_task
        self.mock_repository.update_task.return_value = existing_task

        result = self.service.update_task("test-id", "  New Title  ", "  New Description  ")

        # Check that update_task was called with stripped values
        self.mock_repository.update_task.assert_called_once()
        args = self.mock_repository.update_task.call_args
        assert args[0][0] == "test-id"
        assert args[0][1] == "New Title"  # Title should be stripped
        assert args[0][2] == "New Description"  # Description should be stripped

    def test_update_task_not_found_returns_none(self):
        """Test that updating a non-existent task returns None."""
        self.mock_repository.get_task_by_id.return_value = None

        result = self.service.update_task("non-existent-id", "New Title")

        assert result is None
        self.mock_repository.update_task.assert_not_called()

    def test_delete_task(self):
        """Test deleting a task."""
        self.mock_repository.delete_task.return_value = True

        result = self.service.delete_task("test-id")

        assert result is True
        self.mock_repository.delete_task.assert_called_once_with("test-id")

    def test_toggle_task_status_success(self):
        """Test toggling task status successfully."""
        existing_task = Task(id="test-id", title="Test Task", status=TaskStatus.PENDING)
        toggled_task = Task(id="test-id", title="Test Task", status=TaskStatus.COMPLETED)

        self.mock_repository.get_task_by_id.return_value = existing_task
        self.mock_repository.toggle_task_status.return_value = toggled_task

        result = self.service.toggle_task_status("test-id")

        assert result == toggled_task
        self.mock_repository.toggle_task_status.assert_called_once_with("test-id")

    def test_toggle_task_status_not_found_returns_none(self):
        """Test that toggling status of a non-existent task returns None."""
        self.mock_repository.get_task_by_id.return_value = None

        result = self.service.toggle_task_status("non-existent-id")

        assert result is None
        self.mock_repository.toggle_task_status.assert_not_called()