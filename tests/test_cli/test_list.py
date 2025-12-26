"""Tests for the list CLI command."""

import pytest
from typer.testing import CliRunner
from src.main import app
from src.repositories.memory import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.models.enums import TaskStatus
from src.common import service_manager
from unittest.mock import patch

runner = CliRunner()


class TestListCommand:
    """Test cases for the list CLI command."""

    def setup_method(self):
        """Set up a fresh repository and service for each test."""
        # Reset the service manager to ensure clean state
        service_manager.reset_service()

    def test_list_empty_tasks(self):
        """Test listing when no tasks exist."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "No tasks found" in result.stdout

    def test_list_single_task(self):
        """Test listing a single task."""
        # Add a task first using the CLI
        result_add = runner.invoke(app, ["add", "Test Task", "Test Description"])
        assert result_add.exit_code == 0

        # Now list the tasks
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "Test Task" in result.stdout
        assert "Test Description" in result.stdout

    def test_list_multiple_tasks(self):
        """Test listing multiple tasks."""
        # Add multiple tasks using CLI
        result_add1 = runner.invoke(app, ["add", "First Task", "First Description"])
        result_add2 = runner.invoke(app, ["add", "Second Task", "Second Description"])
        result_add3 = runner.invoke(app, ["add", "Third Task"])  # No description
        assert result_add1.exit_code == 0
        assert result_add2.exit_code == 0
        assert result_add3.exit_code == 0

        # Now list all tasks
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "First Task" in result.stdout
        assert "Second Task" in result.stdout
        assert "Third Task" in result.stdout
        assert "First Description" in result.stdout
        assert "Second Description" in result.stdout

    def test_list_tasks_with_different_statuses(self):
        """Test listing tasks with different statuses."""
        # Add tasks using CLI
        result_add1 = runner.invoke(app, ["add", "Pending Task", "Description for pending"])
        result_add2 = runner.invoke(app, ["add", "Completed Task", "Description for completed"])
        assert result_add1.exit_code == 0
        assert result_add2.exit_code == 0

        # Capture the ID of the second task to toggle it
        output_lines = result_add2.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        # Toggle the second task to completed
        result_toggle = runner.invoke(app, ["toggle", task_id])
        assert result_toggle.exit_code == 0

        # Now list tasks to see different statuses
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "Pending Task" in result.stdout
        assert "Completed Task" in result.stdout
        assert "Completed" in result.stdout  # For the completed task

    def test_list_task_formatting(self):
        """Test that the list command displays tasks in the expected table format."""
        # Add a task using CLI
        result_add = runner.invoke(app, ["add", "Formatted Task", "Formatted Description"])
        assert result_add.exit_code == 0

        # Now list tasks
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        # Check for table elements
        assert "ID" in result.stdout  # Column header
        assert "Title" in result.stdout  # Column header
        assert "Description" in result.stdout  # Column header
        assert "Status" in result.stdout  # Column header
        assert "Formatted Task" in result.stdout  # Task title appears
        assert "Formatted Description" in result.stdout  # Description appears