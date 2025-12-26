"""Integration tests for the list CLI command."""

import pytest
from typer.testing import CliRunner
from src.main import app
from src.repositories.memory import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.models.enums import TaskStatus

runner = CliRunner()


class TestListCommandIntegration:
    """Integration test cases for the list CLI command."""

    def setup_method(self):
        """Set up a fresh repository and service for each test."""
        self.repository = InMemoryTaskRepository()
        self.service = TaskService(self.repository)

    def test_list_after_add_operations(self):
        """Test listing tasks after multiple add operations."""
        # Add several tasks
        result_add1 = runner.invoke(app, ["add", "Task 1", "Description 1"])
        result_add2 = runner.invoke(app, ["add", "Task 2", "Description 2"])
        result_add3 = runner.invoke(app, ["add", "Task 3"])

        assert result_add1.exit_code == 0
        assert result_add2.exit_code == 0
        assert result_add3.exit_code == 0

        # List all tasks
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0

        # Verify all tasks appear in the list
        assert "Task 1" in result_list.stdout
        assert "Task 2" in result_list.stdout
        assert "Task 3" in result_list.stdout
        assert "Description 1" in result_list.stdout
        assert "Description 2" in result_list.stdout

    def test_list_after_update_operations(self):
        """Test listing tasks after update operations."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Original Task", "Original Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        # Update the task
        result_update = runner.invoke(app, ["update", task_id, "Updated Task", "Updated Description"])
        assert result_update.exit_code == 0

        # List tasks to verify the update is reflected
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0

        # The updated task should appear in the list
        assert "Updated Task" in result_list.stdout
        assert "Updated Description" in result_list.stdout
        # Original name should not appear
        assert "Original Task" not in result_list.stdout

    def test_list_after_toggle_operations(self):
        """Test listing tasks after toggle operations."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Toggle Test Task", "Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        # Initially should be pending
        result_list_before = runner.invoke(app, ["list"])
        assert result_list_before.exit_code == 0
        assert "Pending" in result_list_before.stdout

        # Toggle the task status
        result_toggle = runner.invoke(app, ["toggle", task_id])
        assert result_toggle.exit_code == 0

        # List tasks to verify the status change
        result_list_after = runner.invoke(app, ["list"])
        assert result_list_after.exit_code == 0

        # The task should now show as completed
        assert "Completed" in result_list_after.stdout
        # Should no longer show as pending
        assert "Pending" not in result_list_after.stdout.replace("Completed", "")

    def test_list_after_delete_operations(self):
        """Test listing tasks after delete operations."""
        # Add multiple tasks
        result_add1 = runner.invoke(app, ["add", "Task 1", "Description 1"])
        result_add2 = runner.invoke(app, ["add", "Task 2", "Description 2"])
        result_add3 = runner.invoke(app, ["add", "Task 3", "Description 3"])

        assert result_add1.exit_code == 0
        assert result_add2.exit_code == 0
        assert result_add3.exit_code == 0

        # Capture the task ID for the second task
        output_lines = result_add2.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        # List all tasks initially
        result_list_before = runner.invoke(app, ["list"])
        assert result_list_before.exit_code == 0
        assert "Task 1" in result_list_before.stdout
        assert "Task 2" in result_list_before.stdout
        assert "Task 3" in result_list_before.stdout

        # Delete the second task
        result_delete = runner.invoke(app, ["delete", task_id])
        assert result_delete.exit_code == 0

        # List tasks to verify the deletion
        result_list_after = runner.invoke(app, ["list"])
        assert result_list_after.exit_code == 0

        # Task 2 should not appear, but 1 and 3 should
        assert "Task 1" in result_list_after.stdout
        assert "Task 2" not in result_list_after.stdout
        assert "Task 3" in result_list_after.stdout
        assert "Description 1" in result_list_after.stdout
        assert "Description 2" not in result_list_after.stdout
        assert "Description 3" in result_list_after.stdout

    def test_list_empty_after_all_deletes(self):
        """Test listing when all tasks have been deleted."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Task to Delete", "Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        # Delete the task
        result_delete = runner.invoke(app, ["delete", task_id])
        assert result_delete.exit_code == 0

        # List tasks - should show "No tasks found"
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "No tasks found" in result_list.stdout