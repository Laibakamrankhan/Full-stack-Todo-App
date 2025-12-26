"""Tests for the repository interface."""

import pytest
from abc import ABC
from src.repositories.base import TaskRepository


class TestTaskRepositoryInterface:
    """Test cases for the TaskRepository interface."""

    def test_task_repository_is_abstract(self):
        """Test that TaskRepository is an abstract base class."""
        assert issubclass(TaskRepository, ABC)
        assert hasattr(TaskRepository, '__abstractmethods__')
        assert len(TaskRepository.__abstractmethods__) > 0

    def test_task_repository_has_required_methods(self):
        """Test that TaskRepository defines all required methods."""
        abstract_methods = TaskRepository.__abstractmethods__

        expected_methods = {
            'add_task',
            'get_all_tasks',
            'get_task_by_id',
            'update_task',
            'delete_task',
            'toggle_task_status'
        }

        assert expected_methods.issubset(abstract_methods)

    def test_task_repository_method_signatures(self):
        """Test that TaskRepository methods have the expected signatures."""
        # This test verifies that the abstract methods exist
        # Concrete implementations will be tested in integration tests
        assert hasattr(TaskRepository, 'add_task')
        assert hasattr(TaskRepository, 'get_all_tasks')
        assert hasattr(TaskRepository, 'get_task_by_id')
        assert hasattr(TaskRepository, 'update_task')
        assert hasattr(TaskRepository, 'delete_task')
        assert hasattr(TaskRepository, 'toggle_task_status')