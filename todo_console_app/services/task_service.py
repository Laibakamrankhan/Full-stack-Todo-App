"""Task service for the Todo Console App."""

import uuid
from typing import List, Optional
from todo_console_app.models.task import Task
from todo_console_app.models.enums import TaskStatus
from todo_console_app.repositories.base import TaskRepository


class TaskService:
    """Service layer for task operations with business logic and validation."""

    def __init__(self, repository: TaskRepository) -> None:
        """Initialize the task service with a repository."""
        self.repository = repository

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task with validation."""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            title=title.strip(),
            description=description.strip() if description else None,
            status=TaskStatus.PENDING
        )
        return self.repository.add_task(task)

    def list_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.repository.get_all_tasks()

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        return self.repository.get_task_by_id(task_id)

    def update_task(self, task_id: str, title: str, description: Optional[str] = None) -> Optional[Task]:
        """Update a task with validation."""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        # Check if task exists before updating
        existing_task = self.repository.get_task_by_id(task_id)
        if existing_task is None:
            return None

        return self.repository.update_task(task_id, title.strip(), description.strip() if description else None)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        return self.repository.delete_task(task_id)

    def toggle_task_status(self, task_id: str) -> Optional[Task]:
        """Toggle the status of a task."""
        # Check if task exists before toggling
        existing_task = self.repository.get_task_by_id(task_id)
        if existing_task is None:
            return None

        return self.repository.toggle_task_status(task_id)