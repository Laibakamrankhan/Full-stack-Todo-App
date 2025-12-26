"""Enums for the Todo Console App."""

from enum import Enum


class TaskStatus(str, Enum):
    """Status enum for tasks."""

    PENDING = "pending"
    COMPLETED = "completed"