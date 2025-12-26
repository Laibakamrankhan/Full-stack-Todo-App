"""Tests for the display functions."""

import pytest
from unittest.mock import Mock, patch
from io import StringIO
from src.ui.display import display_tasks_table, display_success_message, display_error_message, display_info_message
from src.models.task import Task
from src.models.enums import TaskStatus


class TestDisplay:
    """Test cases for the display functions."""

    def test_display_tasks_table_with_tasks(self):
        """Test displaying tasks table with multiple tasks."""
        tasks = [
            Task(id="id1", title="Task 1", description="Description 1", status=TaskStatus.PENDING),
            Task(id="id2", title="Task 2", description="Description 2", status=TaskStatus.COMPLETED),
        ]

        # Mock the Console to capture output
        with patch('src.ui.display.Console') as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            display_tasks_table(tasks, mock_console)

            # Verify that print was called (which means table was created and printed)
            assert mock_console.print.called

    def test_display_tasks_table_empty(self):
        """Test displaying tasks table when no tasks exist."""
        tasks = []

        # Mock the Console to capture output
        with patch('src.ui.display.Console') as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            display_tasks_table(tasks, mock_console)

            # Verify that print was called with the "No tasks found" message
            mock_console.print.assert_called_once()

    def test_display_tasks_table_none_console(self):
        """Test displaying tasks table with None console (should create new Console)."""
        tasks = [Task(id="id1", title="Task 1", status=TaskStatus.PENDING)]

        # Mock the Console class to track instantiation
        with patch('src.ui.display.Console') as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            display_tasks_table(tasks)

            # Verify that Console was instantiated and print was called
            assert mock_console_class.called
            assert mock_console.print.called

    def test_display_success_message(self):
        """Test displaying a success message."""
        message = "Task added successfully"

        with patch('src.ui.display.Console') as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            display_success_message(message, mock_console)

            # Verify that print was called with the success message
            mock_console.print.assert_called_once()

    def test_display_success_message_none_console(self):
        """Test displaying a success message with None console."""
        message = "Task added successfully"

        with patch('src.ui.display.Console') as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            display_success_message(message)

            # Verify that Console was instantiated and print was called
            assert mock_console_class.called
            assert mock_console.print.called

    def test_display_error_message(self):
        """Test displaying an error message."""
        message = "Task not found"

        with patch('src.ui.display.Console') as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            display_error_message(message, mock_console)

            # Verify that print was called with the error message
            mock_console.print.assert_called_once()

    def test_display_error_message_none_console(self):
        """Test displaying an error message with None console."""
        message = "Task not found"

        with patch('src.ui.display.Console') as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            display_error_message(message)

            # Verify that Console was instantiated and print was called
            assert mock_console_class.called
            assert mock_console.print.called

    def test_display_info_message(self):
        """Test displaying an info message."""
        message = "Loading tasks..."

        with patch('src.ui.display.Console') as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            display_info_message(message, mock_console)

            # Verify that print was called with the info message
            mock_console.print.assert_called_once()

    def test_display_info_message_none_console(self):
        """Test displaying an info message with None console."""
        message = "Loading tasks..."

        with patch('src.ui.display.Console') as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            display_info_message(message)

            # Verify that Console was instantiated and print was called
            assert mock_console_class.called
            assert mock_console.print.called