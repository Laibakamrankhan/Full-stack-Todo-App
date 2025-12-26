"""Repository protocol interface for the Todo Console App."""

from abc import ABC, abstractmethod
from typing import List, Optional
from todo_console_app.models.task import Task


class TaskRepository(ABC):
    """Abstract base class defining the repository interface for tasks."""

    @abstractmethod
    def add_task(self, task: Task) -> Task:
        """Add a new task to the repository."""
        pass

    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the repository."""
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID."""
        pass

    @abstractmethod
    def update_task(self, task_id: str, title: str, description: Optional[str] = None) -> Optional[Task]:
        """Update an existing task with new details."""
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID. Returns True if deletion was successful."""
        pass

    @abstractmethod
    def toggle_task_status(self, task_id: str) -> Optional[Task]:
        """Toggle the completion status of a task."""
        pass