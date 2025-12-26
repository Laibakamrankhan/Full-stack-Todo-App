"""Tests for the in-memory repository implementation."""

import pytest
from src.repositories.memory import InMemoryTaskRepository
from src.models.task import Task
from src.models.enums import TaskStatus


class TestInMemoryTaskRepository:
    """Test cases for the InMemoryTaskRepository."""

    def setup_method(self):
        """Set up a fresh repository for each test."""
        self.repository = InMemoryTaskRepository()

    def test_add_task(self):
        """Test adding a task to the repository."""
        task = Task(id="test-id", title="Test Task")
        result = self.repository.add_task(task)

        assert result == task
        assert len(self.repository.get_all_tasks()) == 1
        assert self.repository.get_task_by_id("test-id") == task

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when repository is empty."""
        tasks = self.repository.get_all_tasks()

        assert tasks == []
        assert len(tasks) == 0

    def test_get_all_tasks_with_data(self):
        """Test getting all tasks when repository has data."""
        task1 = Task(id="id1", title="Task 1")
        task2 = Task(id="id2", title="Task 2")

        self.repository.add_task(task1)
        self.repository.add_task(task2)

        tasks = self.repository.get_all_tasks()

        assert len(tasks) == 2
        assert task1 in tasks
        assert task2 in tasks

    def test_get_task_by_id_found(self):
        """Test getting a task by ID when it exists."""
        task = Task(id="test-id", title="Test Task")
        self.repository.add_task(task)

        result = self.repository.get_task_by_id("test-id")

        assert result == task

    def test_get_task_by_id_not_found(self):
        """Test getting a task by ID when it doesn't exist."""
        result = self.repository.get_task_by_id("non-existent-id")

        assert result is None

    def test_update_task_success(self):
        """Test updating an existing task."""
        original_task = Task(id="test-id", title="Original Title", description="Original Description")
        self.repository.add_task(original_task)

        updated_task = self.repository.update_task("test-id", "New Title", "New Description")

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.id == "test-id"

        # Verify the task was actually updated in the repository
        retrieved_task = self.repository.get_task_by_id("test-id")
        assert retrieved_task.title == "New Title"
        assert retrieved_task.description == "New Description"

    def test_update_task_not_found(self):
        """Test updating a task that doesn't exist."""
        result = self.repository.update_task("non-existent-id", "New Title")

        assert result is None

    def test_delete_task_success(self):
        """Test deleting an existing task."""
        task = Task(id="test-id", title="Test Task")
        self.repository.add_task(task)

        result = self.repository.delete_task("test-id")

        assert result is True
        assert self.repository.get_task_by_id("test-id") is None
        assert len(self.repository.get_all_tasks()) == 0

    def test_delete_task_not_found(self):
        """Test deleting a task that doesn't exist."""
        result = self.repository.delete_task("non-existent-id")

        assert result is False

    def test_toggle_task_status_pending_to_completed(self):
        """Test toggling task status from pending to completed."""
        task = Task(id="test-id", title="Test Task", status=TaskStatus.PENDING)
        self.repository.add_task(task)

        toggled_task = self.repository.toggle_task_status("test-id")

        assert toggled_task is not None
        assert toggled_task.status == TaskStatus.COMPLETED

        # Verify the task status was actually updated in the repository
        retrieved_task = self.repository.get_task_by_id("test-id")
        assert retrieved_task.status == TaskStatus.COMPLETED

    def test_toggle_task_status_completed_to_pending(self):
        """Test toggling task status from completed to pending."""
        task = Task(id="test-id", title="Test Task", status=TaskStatus.COMPLETED)
        self.repository.add_task(task)

        toggled_task = self.repository.toggle_task_status("test-id")

        assert toggled_task is not None
        assert toggled_task.status == TaskStatus.PENDING

        # Verify the task status was actually updated in the repository
        retrieved_task = self.repository.get_task_by_id("test-id")
        assert retrieved_task.status == TaskStatus.PENDING

    def test_toggle_task_status_not_found(self):
        """Test toggling status of a task that doesn't exist."""
        result = self.repository.toggle_task_status("non-existent-id")

        assert result is None

    def test_repository_isolation(self):
        """Test that the repository properly isolates task data."""
        # Add tasks to one repository
        repo1 = InMemoryTaskRepository()
        task1 = Task(id="id1", title="Task 1")
        repo1.add_task(task1)

        # Create another repository
        repo2 = InMemoryTaskRepository()
        task2 = Task(id="id2", title="Task 2")
        repo2.add_task(task2)

        # Verify repositories are isolated
        assert repo1.get_task_by_id("id1") is not None
        assert repo1.get_task_by_id("id2") is None
        assert repo2.get_task_by_id("id2") is not None
        assert repo2.get_task_by_id("id1") is None