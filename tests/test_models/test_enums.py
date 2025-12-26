"""Tests for the enums."""

import pytest
from src.models.enums import TaskStatus


class TestTaskStatus:
    """Test cases for the TaskStatus enum."""

    def test_task_status_values(self):
        """Test that TaskStatus enum has the correct values."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.COMPLETED.value == "completed"

    def test_task_status_string_representation(self):
        """Test that TaskStatus enum values are strings."""
        assert isinstance(TaskStatus.PENDING.value, str)
        assert isinstance(TaskStatus.COMPLETED.value, str)

    def test_task_status_equality(self):
        """Test that TaskStatus enum values can be compared."""
        assert TaskStatus.PENDING == TaskStatus.PENDING
        assert TaskStatus.COMPLETED == TaskStatus.COMPLETED
        assert TaskStatus.PENDING != TaskStatus.COMPLETED

    def test_task_status_membership(self):
        """Test that TaskStatus enum values can be used in membership tests."""
        all_statuses = [TaskStatus.PENDING, TaskStatus.COMPLETED]
        assert TaskStatus.PENDING in all_statuses
        assert TaskStatus.COMPLETED in all_statuses