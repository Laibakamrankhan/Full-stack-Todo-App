"""Common utilities and shared instances for the Todo Console App."""

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from todo_console_app.services.task_service import TaskService

from todo_console_app.repositories.memory import InMemoryTaskRepository
from todo_console_app.repositories.file import FileTaskRepository


class SingletonServiceManager:
    """Singleton manager to provide shared service instances."""

    _instance = None
    _service: Optional['TaskService'] = None

    def __new__(cls) -> 'SingletonServiceManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._service = None
        return cls._instance

    def get_service(self) -> 'TaskService':
        """Get the shared service instance."""
        if self._service is None:
            # Use file-based repository for persistence
            repository = FileTaskRepository()
            from todo_console_app.services.task_service import TaskService  # Avoid circular import
            self._service = TaskService(repository)
        return self._service

    def reset_service(self) -> None:
        """Reset the service instance (useful for testing)."""
        repository = InMemoryTaskRepository()
        from todo_console_app.services.task_service import TaskService  # Avoid circular import
        self._service = TaskService(repository)

    def set_service(self, service: 'TaskService') -> None:
        """Set a specific service instance (useful for testing)."""
        self._service = service


# Global instance manager
service_manager = SingletonServiceManager()