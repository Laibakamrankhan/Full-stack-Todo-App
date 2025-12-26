"""Task model for the Todo Console App."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .enums import TaskStatus


@dataclass
class Task:
    """Represents a single todo task."""

    id: str  # UUID string
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Set default datetime values after initialization."""
        now = datetime.now()
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now

    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update task fields and set updated_at timestamp."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()

    def toggle_status(self) -> None:
        """Toggle the task status between pending and completed."""
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.COMPLETED
        else:
            self.status = TaskStatus.PENDING
        self.updated_at = datetime.now()