"""Integration tests for the add CLI command."""

import pytest
from typer.testing import CliRunner
from src.main import app
from src.repositories.memory import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.models.task import Task

runner = CliRunner()


class TestAddCommandIntegration:
    """Integration test cases for the add CLI command."""

    def setup_method(self):
        """Set up a fresh repository and service for each test."""
        self.repository = InMemoryTaskRepository()
        self.service = TaskService(self.repository)

    def test_add_task_then_list(self):
        """Test adding a task and then listing it."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Test Task", "Test Description"])
        assert result_add.exit_code == 0
        assert "Task added successfully" in result_add.stdout

        # List tasks to verify it was added
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Test Task" in result_list.stdout
        assert "Test Description" in result_list.stdout

    def test_add_multiple_tasks_then_list(self):
        """Test adding multiple tasks and then listing them."""
        # Add first task
        result_add1 = runner.invoke(app, ["add", "First Task", "First Description"])
        assert result_add1.exit_code == 0
        assert "Task added successfully" in result_add1.stdout

        # Add second task
        result_add2 = runner.invoke(app, ["add", "Second Task", "Second Description"])
        assert result_add2.exit_code == 0
        assert "Task added successfully" in result_add2.stdout

        # List tasks to verify both were added
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "First Task" in result_list.stdout
        assert "Second Task" in result_list.stdout
        assert "First Description" in result_list.stdout
        assert "Second Description" in result_list.stdout

    def test_add_task_then_update(self):
        """Test adding a task and then updating it."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Original Task", "Original Description"])
        assert result_add.exit_code == 0
        assert "Task added successfully" in result_add.stdout

        # Capture the task ID from the output
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None, "Task ID should be captured from add command output"

        # Update the task
        result_update = runner.invoke(app, ["update", task_id, "Updated Task", "Updated Description"])
        assert result_update.exit_code == 0
        assert "Task updated successfully" in result_update.stdout

        # List tasks to verify update
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Updated Task" in result_list.stdout
        assert "Updated Description" in result_list.stdout

    def test_add_task_then_delete(self):
        """Test adding a task and then deleting it."""
        # Add a task
        result_add = runner.invoke(app, ["add", "Task to Delete", "Description to Delete"])
        assert result_add.exit_code == 0
        assert "Task added successfully" in result_add.stdout

        # Capture the task ID from the output
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None, "Task ID should be captured from add command output"

        # Delete the task
        result_delete = runner.invoke(app, ["delete", task_id])
        assert result_delete.exit_code == 0
        assert "Task deleted successfully" in result_delete.stdout

        # List tasks to verify deletion
        result_list = runner.invoke(app, ["list"])
        assert result_list.exit_code == 0
        assert "Task to Delete" not in result_list.stdout
        assert "Description to Delete" not in result_list.stdout