"""Integration tests for the delete CLI command."""

import pytest
from typer.testing import CliRunner
from src.main import app
from src.repositories.memory import InMemoryTaskRepository
from src.services.task_service import TaskService

runner = CliRunner()


class TestDeleteCommandIntegration:
    """Integration test cases for the delete CLI command."""

    def setup_method(self):
        """Set up a fresh repository and service for each test."""
        self.repository = InMemoryTaskRepository()
        self.service = TaskService(self.repository)

    def test_delete_then_list_verification(self):
        """Test deleting a task and then verifying it's gone with list."""
        # Add multiple tasks
        result_add1 = runner.invoke(app, ["add", "Task 1", "Description 1"])
        result_add2 = runner.invoke(app, ["add", "Task 2", "Description 2"])
        result_add3 = runner.invoke(app, ["add", "Task 3", "Description 3"])
        assert result_add1.exit_code == 0
        assert result_add2.exit_code == 0
        assert result_add3.exit_code == 0

        # Capture task IDs
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

        # Delete one task
        result_delete = runner.invoke(app, ["delete", task_id])
        assert result_delete.exit_code == 0
        assert "Task deleted successfully" in result_delete.stdout

        # List tasks to verify deletion
        result_list_after = runner.invoke(app, ["list"])
        assert result_list_after.exit_code == 0
        assert "Task 1" in result_list_after.stdout
        assert "Task 2" not in result_list_after.stdout  # This was the deleted task
        assert "Task 3" in result_list_after.stdout

    def test_delete_then_add_verification(self):
        """Test deleting a task and then adding a new one."""
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
        assert "Task deleted successfully" in result_delete.stdout

        # List to verify it's gone
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Task to Delete" not in result_list.stdout

        # Add a new task
        result_add_new = runner.invoke(app, ["add", "New Task", "New Description"])
        assert result_add_new.exit_code == 0
        assert "Task added successfully" in result_add_new.stdout

        # List to verify new task exists
        result_list_new = runner.invoke(app, ["list"])
        assert result_list_new.exit_code == 0
        assert "New Task" in result_list_new.stdout
        assert "New Description" in result_list_new.stdout

    def test_delete_then_update_other_verification(self):
        """Test deleting one task and then updating another."""
        # Add two tasks
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

        # Delete the first task
        result_delete = runner.invoke(app, ["delete", task_id1])
        assert result_delete.exit_code == 0
        assert "Task deleted successfully" in result_delete.stdout

        # Update the second task
        result_update = runner.invoke(app, ["update", task_id2, "Updated Task 2", "Updated Description 2"])
        assert result_update.exit_code == 0
        assert "Task updated successfully" in result_update.stdout

        # List to verify first task is gone and second is updated
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Task 1" not in result_list.stdout  # Should be deleted
        assert "Task 2" not in result_list.stdout  # Should be updated
        assert "Updated Task 2" in result_list.stdout  # Should show updated name
        assert "Updated Description 2" in result_list.stdout  # Should show updated description

    def test_delete_then_toggle_verification(self):
        """Test deleting one task and then toggling another."""
        # Add two tasks
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

        # Delete the first task
        result_delete = runner.invoke(app, ["delete", task_id1])
        assert result_delete.exit_code == 0
        assert "Task deleted successfully" in result_delete.stdout

        # Toggle the second task
        result_toggle = runner.invoke(app, ["toggle", task_id2])
        assert result_toggle.exit_code == 0
        assert "Task status toggled successfully" in result_toggle.stdout

        # List to verify first task is gone and second has toggled status
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Task 1" not in result_list.stdout  # Should be deleted
        assert "Task 2" in result_list.stdout  # Should still exist
        assert "Completed" in result_list.stdout  # Should show completed status

    def test_delete_non_existent_task_no_impact(self):
        """Test deleting a non-existent task doesn't impact existing tasks."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Existing Task", "Description"])
        assert result_add.exit_code == 0

        # Try to delete a non-existent task
        result_delete = runner.invoke(app, ["delete", "non-existent-id"])
        assert result_delete.exit_code == 0
        assert "Error: Task with ID non-existent-id not found" in result_delete.stdout

        # List to verify the existing task is still there
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Existing Task" in result_list.stdout
        assert "Description" in result_list.stdout