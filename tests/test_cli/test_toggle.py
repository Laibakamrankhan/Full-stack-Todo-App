"""Tests for the toggle CLI command."""

import pytest
from typer.testing import CliRunner
from src.main import app
from src.repositories.memory import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.models.enums import TaskStatus
from src.common import service_manager
from unittest.mock import patch

runner = CliRunner()


class TestToggleCommand:
    """Test cases for the toggle CLI command."""

    def setup_method(self):
        """Set up a fresh repository and service for each test."""
        # Reset the service manager to ensure clean state
        service_manager.reset_service()

    def test_toggle_task_from_pending_to_completed(self):
        """Test toggling a task from pending to completed."""
        # Add a task using CLI (defaults to pending)
        result_add = runner.invoke(app, ["add", "Test Task", "Test Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        result = runner.invoke(app, ["toggle", task_id])

        assert result.exit_code == 0
        assert "Task status toggled successfully" in result.stdout

        # Verify the task status was updated by listing
        result_list = runner.invoke(app, ["list"])
        assert "Completed" in result_list.stdout

    def test_toggle_task_from_completed_to_pending(self):
        """Test toggling a task from completed to pending."""
        # Add a task and toggle it to completed first
        result_add = runner.invoke(app, ["add", "Test Task", "Test Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        # First toggle to make it completed
        result_toggle1 = runner.invoke(app, ["toggle", task_id])
        assert result_toggle1.exit_code == 0
        assert "Task status toggled successfully" in result_toggle1.stdout

        # Verify it's completed
        result_list1 = runner.invoke(app, ["list"])
        assert "Completed" in result_list1.stdout

        # Toggle again to make it pending
        result_toggle2 = runner.invoke(app, ["toggle", task_id])
        assert result_toggle2.exit_code == 0
        assert "Task status toggled successfully" in result_toggle2.stdout

        # Verify the task status was updated back to pending by listing
        result_list2 = runner.invoke(app, ["list"])
        assert "Pending" in result_list2.stdout

    def test_toggle_non_existent_task_error(self):
        """Test toggling a non-existent task shows error."""
        result = runner.invoke(app, ["toggle", "non-existent-id"])

        assert result.exit_code == 0  # Command completes but shows error
        assert "Error: Task with ID non-existent-id not found" in result.stdout

    def test_multiple_toggles_cycling_status(self):
        """Test multiple toggles cycle the status correctly."""
        # Add a task using CLI (defaults to pending)
        result_add = runner.invoke(app, ["add", "Test Task", "Test Description"])
        assert result_add.exit_code == 0

        # Capture the task ID
        output_lines = result_add.stdout.split('\n')
        task_id = None
        for line in output_lines:
            if "Task added successfully with ID:" in line:
                task_id = line.split("ID: ")[1].strip()
                break

        assert task_id is not None

        # Toggle 1: pending -> completed
        result1 = runner.invoke(app, ["toggle", task_id])
        assert result1.exit_code == 0
        assert "Task status toggled successfully" in result1.stdout

        result_list1 = runner.invoke(app, ["list"])
        assert "Completed" in result_list1.stdout

        # Toggle 2: completed -> pending
        result2 = runner.invoke(app, ["toggle", task_id])
        assert result2.exit_code == 0
        assert "Task status toggled successfully" in result2.stdout

        result_list2 = runner.invoke(app, ["list"])
        assert "Pending" in result_list2.stdout

        # Toggle 3: pending -> completed
        result3 = runner.invoke(app, ["toggle", task_id])
        assert result3.exit_code == 0
        assert "Task status toggled successfully" in result3.stdout

        result_list3 = runner.invoke(app, ["list"])
        assert "Completed" in result_list3.stdout

    def test_toggle_then_verify_with_list(self):
        """Test toggling a task and then verifying status with list command."""
        # Add a task using CLI (defaults to pending)
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
        assert "Pending" in result_list_before.stdout

        # Toggle the task
        result_toggle = runner.invoke(app, ["toggle", task_id])
        assert result_toggle.exit_code == 0
        assert "Task status toggled successfully" in result_toggle.stdout

        # After toggle, should be completed
        result_list_after = runner.invoke(app, ["list"])
        assert "Completed" in result_list_after.stdout
        # Should no longer show as pending
        assert "Pending" not in result_list_after.stdout.replace("Completed", "")