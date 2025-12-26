"""In-memory repository implementation for the Todo Console App."""

from typing import List, Optional
from .base import TaskRepository
from todo_console_app.models.task import Task


class InMemoryTaskRepository(TaskRepository):
    """In-memory implementation of the TaskRepository interface."""

    def __init__(self) -> None:
        """Initialize the in-memory repository with an empty task list."""
        self._tasks: List[Task] = []

    def add_task(self, task: Task) -> Task:
        """Add a new task to the repository."""
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the repository."""
        return self._tasks.copy()  # Return a copy to prevent external modification

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: str, title: str, description: Optional[str] = None) -> Optional[Task]:
        """Update an existing task with new details."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        task.update(title=title, description=description)
        return task

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID. Returns True if deletion was successful."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self._tasks.remove(task)
        return True

    def toggle_task_status(self, task_id: str) -> Optional[Task]:
        """Toggle the completion status of a task."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        task.toggle_status()
        return task