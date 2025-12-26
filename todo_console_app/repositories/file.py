"""File-based task repository implementation for persistent storage."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from .base import TaskRepository
from ..models.task import Task
from ..models.enums import TaskStatus


class FileTaskRepository(TaskRepository):
    """File-based implementation of TaskRepository with JSON persistence."""

    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Ensure the tasks file exists, create it with empty list if not."""
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def _load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from the JSON file."""
        try:
            content = self.file_path.read_text(encoding="utf-8")
            return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Save tasks to the JSON file."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False, default=str)

    def _dict_to_task(self, task_dict: Dict[str, Any]) -> Task:
        """Convert dictionary to Task object."""
        # Convert string datetime back to datetime object
        created_at = datetime.fromisoformat(task_dict["created_at"]) if task_dict["created_at"] else None
        updated_at = datetime.fromisoformat(task_dict["updated_at"]) if task_dict["updated_at"] else None

        return Task(
            id=task_dict["id"],
            title=task_dict["title"],
            description=task_dict["description"],
            status=TaskStatus(task_dict["status"]),
            created_at=created_at,
            updated_at=updated_at
        )

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """Convert Task object to dictionary."""
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }

    def add_task(self, task: Task) -> Task:
        """Add a new task to the repository."""
        tasks = self._load_tasks()

        # Check if task already exists
        for existing_task in tasks:
            if existing_task["id"] == task.id:
                raise ValueError(f"Task with ID {task.id} already exists")

        tasks.append(self._task_to_dict(task))
        self._save_tasks(tasks)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from the repository."""
        tasks_data = self._load_tasks()
        return [self._dict_to_task(task_data) for task_data in tasks_data]

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID."""
        tasks_data = self._load_tasks()
        for task_data in tasks_data:
            if task_data["id"] == task_id:
                return self._dict_to_task(task_data)
        return None

    def update_task(self, task_id: str, title: str, description: Optional[str] = None) -> Optional[Task]:
        """Update an existing task with new details."""
        tasks = self._load_tasks()
        for i, task_data in enumerate(tasks):
            if task_data["id"] == task_id:
                # Create updated task with new details
                current_task = self._dict_to_task(task_data)
                current_task.update(title=title, description=description)
                tasks[i] = self._task_to_dict(current_task)
                self._save_tasks(tasks)
                return current_task
        return None

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        tasks = self._load_tasks()
        initial_length = len(tasks)
        tasks = [task for task in tasks if task["id"] != task_id]

        if len(tasks) < initial_length:
            self._save_tasks(tasks)
            return True
        return False

    def toggle_task_status(self, task_id: str) -> Optional[Task]:
        """Toggle the status of a task."""
        tasks = self._load_tasks()
        for i, task_data in enumerate(tasks):
            if task_data["id"] == task_id:
                # Create updated task with toggled status
                current_task = self._dict_to_task(task_data)
                current_task.toggle_status()
                tasks[i] = self._task_to_dict(current_task)
                self._save_tasks(tasks)
                return current_task
        return None