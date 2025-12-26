"""Integration tests for the toggle CLI command."""

import pytest
from typer.testing import CliRunner
from src.main import app
from src.repositories.memory import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.models.enums import TaskStatus

runner = CliRunner()


class TestToggleCommandIntegration:
    """Integration test cases for the toggle CLI command."""

    def setup_method(self):
        """Set up a fresh repository and service for each test."""
        self.repository = InMemoryTaskRepository()
        self.service = TaskService(self.repository)

    def test_toggle_then_list_verification(self):
        """Test toggling a task and then verifying the status change with list."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Toggle Test Task", "Description"])
        assert result_add.exit_code == 0
        assert "Task added successfully" in result_add.stdout

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

        # Toggle the task
        result_toggle = runner.invoke(app, ["toggle", task_id])
        assert result_toggle.exit_code == 0
        assert "Task status toggled successfully" in result_toggle.stdout

        # After toggle, should be completed
        result_list_after = runner.invoke(app, ["list"])
        assert result_list_after.exit_code == 0
        assert "Completed" in result_list_after.stdout
        # Should no longer show as pending
        assert "Pending" not in result_list_after.stdout.replace("Completed", "")

    def test_toggle_then_update_verification(self):
        """Test toggling a task and then updating it."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Toggle Then Update Task", "Original Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        # Toggle the task status
        result_toggle = runner.invoke(app, ["toggle", task_id])
        assert result_toggle.exit_code == 0
        assert "Task status toggled successfully" in result_toggle.stdout

        # Update the task details
        result_update = runner.invoke(app, ["update", task_id, "Updated Toggle Task", "Updated Description"])
        assert result_update.exit_code == 0
        assert "Task updated successfully" in result_update.stdout

        # List to verify both status change and update
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Updated Toggle Task" in result_list.stdout
        assert "Updated Description" in result_list.stdout
        assert "Completed" in result_list.stdout  # Should still be completed

    def test_toggle_then_delete_verification(self):
        """Test toggling a task and then deleting it."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Toggle Then Delete Task", "Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        # Toggle the task status
        result_toggle = runner.invoke(app, ["toggle", task_id])
        assert result_toggle.exit_code == 0
        assert "Task status toggled successfully" in result_toggle.stdout

        # Verify it's completed
        result_list_before_delete = runner.invoke(app, ["list"])
        assert result_list_before_delete.exit_code == 0
        assert "Completed" in result_list_before_delete.stdout

        # Delete the task
        result_delete = runner.invoke(app, ["delete", task_id])
        assert result_delete.exit_code == 0
        assert "Task deleted successfully" in result_delete.stdout

        # Verify it's gone
        result_list_after_delete = runner.invoke(app, ["list"])
        assert result_list_after_delete.exit_code == 0
        assert "Toggle Then Delete Task" not in result_list_after_delete.stdout
        assert "Completed" not in result_list_after_delete.stdout

    def test_multiple_toggles_with_multiple_tasks(self):
        """Test toggling multiple tasks independently."""
        # Add multiple tasks
        result_add1 = runner.invoke(app, ["add", "Task 1", "Description 1"])
        result_add2 = runner.invoke(app, ["add", "Task 2", "Description 2"])
        result_add3 = runner.invoke(app, ["add", "Task 3", "Description 3"])
        assert result_add1.exit_code == 0
        assert result_add2.exit_code == 0
        assert result_add3.exit_code == 0

        # Capture task IDs
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

        output_lines3 = result_add3.stdout.split('\n')
        task_id3 = None
        for line in output_lines3:
            if "Task added successfully with ID:" in line:
                task_id3 = line.split("ID: ")[1].strip()
                break

        assert task_id1 and task_id2 and task_id3

        # Initially all should be pending
        result_list_initial = runner.invoke(app, ["list"])
        assert result_list_initial.exit_code == 0
        pending_count = result_list_initial.stdout.count("Pending")
        completed_count = result_list_initial.stdout.count("Completed")
        assert pending_count >= 3  # At least 3 pending (might be more due to table headers)
        assert completed_count == 0

        # Toggle task 1: pending -> completed
        result_toggle1 = runner.invoke(app, ["toggle", task_id1])
        assert result_toggle1.exit_code == 0
        assert "Task status toggled successfully" in result_toggle1.stdout

        # Toggle task 2: pending -> completed
        result_toggle2 = runner.invoke(app, ["toggle", task_id2])
        assert result_toggle2.exit_code == 0
        assert "Task status toggled successfully" in result_toggle2.stdout

        # List to verify: task 1 and 2 are completed, task 3 is pending
        result_list_after_toggles = runner.invoke(app, ["list"])
        assert result_list_after_toggles.exit_code == 0

        # Verify specific tasks have correct status
        assert task_id1 in result_list_after_toggles.stdout
        assert task_id2 in result_list_after_toggles.stdout
        assert task_id3 in result_list_after_toggles.stdout

        # Count completed and pending after toggles
        completed_count_after = result_list_after_toggles.stdout.count("Completed")
        pending_count_after = result_list_after_toggles.stdout.count("Pending") - completed_count_after  # Adjust for table headers

        # Should have 2 completed and 1 pending (plus any table header occurrences)
        assert completed_count_after >= 2

    def test_toggle_non_existent_task_no_impact(self):
        """Test toggling a non-existent task doesn't impact existing tasks."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Existing Task", "Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        # Try to toggle a non-existent task
        result_toggle = runner.invoke(app, ["toggle", "non-existent-id"])
        assert result_toggle.exit_code == 0
        assert "Error: Task with ID non-existent-id not found" in result_toggle.stdout

        # List to verify the existing task is still there with original status
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Existing Task" in result_list.stdout
        assert "Description" in result_list.stdout
        assert "Pending" in result_list.stdout  # Should still be pending