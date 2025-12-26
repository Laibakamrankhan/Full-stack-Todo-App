"""Integration tests for the update CLI command."""

import pytest
from typer.testing import CliRunner
from src.main import app
from src.repositories.memory import InMemoryTaskRepository
from src.services.task_service import TaskService

runner = CliRunner()


class TestUpdateCommandIntegration:
    """Integration test cases for the update CLI command."""

    def setup_method(self):
        """Set up a fresh repository and service for each test."""
        self.repository = InMemoryTaskRepository()
        self.service = TaskService(self.repository)

    def test_update_then_list_verification(self):
        """Test updating a task and then verifying the change with list."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Original Task", "Original Description"])
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

        # Update the task
        result_update = runner.invoke(app, ["update", task_id, "Updated Task", "Updated Description"])
        assert result_update.exit_code == 0
        assert "Task updated successfully" in result_update.stdout

        # List tasks to verify the update
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Updated Task" in result_list.stdout
        assert "Updated Description" in result_list.stdout
        assert "Original Task" not in result_list.stdout
        assert "Original Description" not in result_list.stdout

    def test_update_then_toggle_verification(self):
        """Test updating a task and then toggling its status."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Task to Update", "Description"])
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
        result_update = runner.invoke(app, ["update", task_id, "Updated Task Title", "Updated Description"])
        assert result_update.exit_code == 0
        assert "Task updated successfully" in result_update.stdout

        # Toggle the task status
        result_toggle = runner.invoke(app, ["toggle", task_id])
        assert result_toggle.exit_code == 0
        assert "Task status toggled successfully" in result_toggle.stdout

        # List tasks to verify both update and toggle
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Updated Task Title" in result_list.stdout
        assert "Updated Description" in result_list.stdout

    def test_update_then_delete_verification(self):
        """Test updating a task and then deleting it."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Task to Update and Delete", "Original Description"])
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
        assert "Task updated successfully" in result_update.stdout

        # Verify the update by listing
        result_list_before_delete = runner.invoke(app, ["list"])
        assert result_list_before_delete.exit_code == 0
        assert "Updated Task" in result_list_before_delete.stdout
        assert "Updated Description" in result_list_before_delete.stdout

        # Delete the task
        result_delete = runner.invoke(app, ["delete", task_id])
        assert result_delete.exit_code == 0
        assert "Task deleted successfully" in result_delete.stdout

        # Verify deletion by listing
        result_list_after_delete = runner.invoke(app, ["list"])
        assert result_list_after_delete.exit_code == 0
        assert "Updated Task" not in result_list_after_delete.stdout
        assert "Updated Description" not in result_list_after_delete.stdout

    def test_multiple_updates_to_same_task(self):
        """Test multiple updates to the same task."""
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

        # First update
        result_update1 = runner.invoke(app, ["update", task_id, "First Updated Task", "First Updated Description"])
        assert result_update1.exit_code == 0
        assert "Task updated successfully" in result_update1.stdout

        # Second update
        result_update2 = runner.invoke(app, ["update", task_id, "Second Updated Task", "Second Updated Description"])
        assert result_update2.exit_code == 0
        assert "Task updated successfully" in result_update2.stdout

        # List tasks to verify the final state
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Second Updated Task" in result_list.stdout
        assert "Second Updated Description" in result_list.stdout
        assert "First Updated Task" not in result_list.stdout
        assert "Original Task" not in result_list.stdout

    def test_update_task_with_special_characters(self):
        """Test updating a task with special characters in title and description."""
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

        # Update with special characters
        special_title = "Task with @#$%^&*() special chars"
        special_description = "Description with [brackets] and {braces} and more $%^&*"

        result_update = runner.invoke(app, ["update", task_id, special_title, special_description])
        assert result_update.exit_code == 0
        assert "Task updated successfully" in result_update.stdout

        # List tasks to verify special characters were preserved
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert special_title in result_list.stdout
        assert special_description in result_list.stdout