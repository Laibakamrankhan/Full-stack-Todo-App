"""Tests for the delete CLI command."""

import pytest
from typer.testing import CliRunner
from src.main import app
from src.repositories.memory import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.common import service_manager
from unittest.mock import patch

runner = CliRunner()


class TestDeleteCommand:
    """Test cases for the delete CLI command."""

    def setup_method(self):
        """Set up a fresh repository and service for each test."""
        # Reset the service manager to ensure clean state
        service_manager.reset_service()

    def test_delete_existing_task(self):
        """Test deleting an existing task."""
        # Add a task first using CLI
        result_add = runner.invoke(app, ["add", "Task to Delete", "Description to Delete"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        result = runner.invoke(app, ["delete", task_id])

        assert result.exit_code == 0
        assert "Task deleted successfully" in result.stdout

        # Verify the task was deleted by listing
        result_list = runner.invoke(app, ["list"])
        assert "Task to Delete" not in result_list.stdout
        assert "Description to Delete" not in result_list.stdout

    def test_delete_non_existent_task_error(self):
        """Test deleting a non-existent task shows error."""
        result = runner.invoke(app, ["delete", "non-existent-id"])

        assert result.exit_code == 0  # Command completes but shows error
        assert "Error: Task with ID non-existent-id not found" in result.stdout

    def test_delete_task_then_verify_absence(self):
        """Test deleting a task and then verifying it's no longer in the repository."""
        # Add multiple tasks using CLI
        result_add1 = runner.invoke(app, ["add", "Task 1", "Description 1"])
        result_add2 = runner.invoke(app, ["add", "Task 2", "Description 2"])
        result_add3 = runner.invoke(app, ["add", "Task 3", "Description 3"])
        assert result_add1.exit_code == 0
        assert result_add2.exit_code == 0
        assert result_add3.exit_code == 0

        # Verify all tasks exist initially by listing
        result_list_before = runner.invoke(app, ["list"])
        assert "Task 1" in result_list_before.stdout
        assert "Task 2" in result_list_before.stdout
        assert "Task 3" in result_list_before.stdout

        # Capture the ID of task2 to delete
        output_lines = result_add2.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        result = runner.invoke(app, ["delete", task_id])

        assert result.exit_code == 0
        assert "Task deleted successfully" in result.stdout

        # Verify task2 was deleted but others remain by listing
        result_list_after = runner.invoke(app, ["list"])
        assert "Task 1" in result_list_after.stdout
        assert "Task 2" not in result_list_after.stdout  # Should be deleted
        assert "Task 3" in result_list_after.stdout

    def test_delete_all_tasks(self):
        """Test deleting all tasks one by one."""
        # Add multiple tasks using CLI
        result_add1 = runner.invoke(app, ["add", "Task 1", "Description 1"])
        result_add2 = runner.invoke(app, ["add", "Task 2", "Description 2"])
        assert result_add1.exit_code == 0
        assert result_add2.exit_code == 0

        # Capture both task IDs
        output_lines1 = result_add1.stdout.split('\n')
        task_id1 = None
        for line in output_lines1:
            if "Task added successfully with ID:" in line:
                task_id1 = line.split("ID: ")[1].strip()
                break

        output_lines2 = result_add2.stdout.split('\n')
        task_id2 = None
        for line in output_lines2:
            if "Task added successfully with ID:" in line:
                task_id2 = line.split("ID: ")[1].strip()
                break

        assert task_id1 is not None
        assert task_id2 is not None

        # Delete first task
        result1 = runner.invoke(app, ["delete", task_id1])
        assert result1.exit_code == 0
        assert "Task deleted successfully" in result1.stdout

        # Verify only one task remains by listing
        result_list_middle = runner.invoke(app, ["list"])
        assert "Task 1" not in result_list_middle.stdout
        assert "Task 2" in result_list_middle.stdout

        # Delete second task
        result2 = runner.invoke(app, ["delete", task_id2])
        assert result2.exit_code == 0
        assert "Task deleted successfully" in result2.stdout

        # Verify no tasks remain by listing
        result_list_final = runner.invoke(app, ["list"])
        assert "No tasks found" in result_list_final.stdout