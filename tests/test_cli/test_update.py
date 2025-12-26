"""Tests for the update CLI command."""

import pytest
from typer.testing import CliRunner
from src.main import app
from src.repositories.memory import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.common import service_manager
from unittest.mock import patch

runner = CliRunner()


class TestUpdateCommand:
    """Test cases for the update CLI command."""

    def setup_method(self):
        """Set up a fresh repository and service for each test."""
        # Reset the service manager to ensure clean state
        service_manager.reset_service()

    def test_update_task_with_new_title_and_description(self):
        """Test updating a task with new title and description."""
        # Add a task first using CLI
        result_add = runner.invoke(app, ["add", "Original Title", "Original Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        result = runner.invoke(app, ["update", task_id, "New Title", "New Description"])

        assert result.exit_code == 0
        assert "Task updated successfully" in result.stdout

        # Verify the task was updated by listing
        result_list = runner.invoke(app, ["list"])
        assert "New Title" in result_list.stdout
        assert "New Description" in result_list.stdout
        assert "Original Title" not in result_list.stdout
        assert "Original Description" not in result_list.stdout

    def test_update_task_with_new_title_only(self):
        """Test updating a task with only a new title."""
        # Add a task first using CLI
        result_add = runner.invoke(app, ["add", "Original Title", "Original Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        result = runner.invoke(app, ["update", task_id, "New Title"])

        assert result.exit_code == 0
        assert "Task updated successfully" in result.stdout

        # Verify the task was updated by listing (title changed, description unchanged)
        result_list = runner.invoke(app, ["list"])
        assert "New Title" in result_list.stdout
        assert "Original Description" in result_list.stdout  # Should remain unchanged
        assert "Original Title" not in result_list.stdout

    def test_update_task_not_found_error(self):
        """Test updating a non-existent task shows error."""
        result = runner.invoke(app, ["update", "non-existent-id", "New Title"])

        assert result.exit_code == 0  # Command completes but shows error
        assert "Error: Task with ID non-existent-id not found" in result.stdout

    def test_update_task_empty_title_error(self):
        """Test that updating a task with empty title shows error."""
        # Add a task first using CLI
        result_add = runner.invoke(app, ["add", "Original Title", "Original Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        result = runner.invoke(app, ["update", task_id, ""])

        assert result.exit_code == 0  # Command completes but shows error
        assert "Task title cannot be empty" in result.stdout

        # Verify the task was not updated by listing
        result_list = runner.invoke(app, ["list"])
        assert "Original Title" in result_list.stdout  # Should remain unchanged

    def test_update_task_whitespace_only_title_error(self):
        """Test that updating a task with whitespace-only title shows error."""
        # Add a task first using CLI
        result_add = runner.invoke(app, ["add", "Original Title", "Original Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        result = runner.invoke(app, ["update", task_id, "   "])

        assert result.exit_code == 0  # Command completes but shows error
        assert "Task title cannot be empty" in result.stdout

        # Verify the task was not updated by listing
        result_list = runner.invoke(app, ["list"])
        assert "Original Title" in result_list.stdout  # Should remain unchanged

    def test_update_task_strips_whitespace(self):
        """Test that updated task title and description are automatically stripped."""
        # Add a task first using CLI
        result_add = runner.invoke(app, ["add", "Original Title", "Original Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        result = runner.invoke(app, ["update", task_id, "  New Title  ", "  New Description  "])

        assert result.exit_code == 0
        assert "Task updated successfully" in result.stdout

        # Verify the task was updated with stripped values by listing
        result_list = runner.invoke(app, ["list"])
        assert "New Title" in result_list.stdout  # Should be stripped
        assert "New Description" in result_list.stdout  # Should be stripped
        assert "Original Title" not in result_list.stdout