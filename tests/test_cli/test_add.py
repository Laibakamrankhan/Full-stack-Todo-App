"""Tests for the add CLI command."""

import pytest
from typer.testing import CliRunner
from src.main import app
from src.repositories.memory import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.common import service_manager
from unittest.mock import patch, Mock

runner = CliRunner()


class TestAddCommand:
    """Test cases for the add CLI command."""

    def setup_method(self):
        """Set up a fresh repository and service for each test."""
        # Reset the service manager to ensure clean state
        service_manager.reset_service()

    def test_add_task_with_title_only(self):
        """Test adding a task with only a title."""
        result = runner.invoke(app, ["add", "Test Task"])

        assert result.exit_code == 0
        assert "Task added successfully" in result.stdout

        # Check that the task was added to the shared service
        service = service_manager.get_service()
        tasks = service.list_tasks()
        assert len(tasks) == 1

        task = tasks[0]
        assert task.title == "Test Task"
        assert task.description is None

    def test_add_task_with_title_and_description(self):
        """Test adding a task with both title and description."""
        result = runner.invoke(app, ["add", "Test Task", "Test Description"])

        assert result.exit_code == 0
        assert "Task added successfully" in result.stdout

        service = service_manager.get_service()
        tasks = service.list_tasks()
        assert len(tasks) == 1

        task = tasks[0]
        assert task.title == "Test Task"
        assert task.description == "Test Description"

    def test_add_task_empty_title_error(self):
        """Test that adding a task with empty title shows error."""
        result = runner.invoke(app, ["add", ""])

        assert result.exit_code == 0  # Command completes but shows error
        assert "Task title cannot be empty" in result.stdout

        service = service_manager.get_service()
        tasks = service.list_tasks()
        assert len(tasks) == 0

    def test_add_task_whitespace_only_title_error(self):
        """Test that adding a task with whitespace-only title shows error."""
        result = runner.invoke(app, ["add", "   "])

        assert result.exit_code == 0  # Command completes but shows error
        assert "Task title cannot be empty" in result.stdout

        service = service_manager.get_service()
        tasks = service.list_tasks()
        assert len(tasks) == 0

    def test_add_task_strips_whitespace(self):
        """Test that task title and description are automatically stripped."""
        result = runner.invoke(app, ["add", "  Test Task  ", "  Test Description  "])

        assert result.exit_code == 0
        assert "Task added successfully" in result.stdout

        service = service_manager.get_service()
        tasks = service.list_tasks()
        assert len(tasks) == 1

        task = tasks[0]
        assert task.title == "Test Task"  # Should be stripped
        assert task.description == "Test Description"  # Should be stripped