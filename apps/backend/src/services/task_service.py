from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
import logging


logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_task(self, task_create: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for the specified user.
        """
        logger.info(f"Creating new task for user: {user_id}")

        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            category=task_create.category,
            user_id=user_id
        )

        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

        logger.info(f"Successfully created task: {db_task.id} for user: {user_id}")

        return db_task

    def get_tasks_by_user(self, user_id: str, completed: Optional[bool] = None) -> List[Task]:
        """
        Get all tasks for a specific user, optionally filtered by completion status.
        """
        logger.info(f"Retrieving tasks for user: {user_id}, completed filter: {completed}")

        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.completed == completed)

        tasks = self.db_session.exec(query).all()

        logger.info(f"Retrieved {len(tasks)} tasks for user: {user_id}")

        return tasks

    def get_task_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for the specified user.
        """
        logger.info(f"Retrieving task {task_id} for user: {user_id}")

        task = self.db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if task:
            logger.info(f"Found task {task_id} for user: {user_id}")
        else:
            logger.warning(f"Task {task_id} not found for user: {user_id}")

        return task

    def update_task(self, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        """
        Update a specific task by ID for the specified user.
        """
        logger.info(f"Updating task {task_id} for user: {user_id}")

        db_task = self.db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not db_task:
            logger.warning(f"Cannot update task {task_id}: not found for user: {user_id}")
            return None

        # Update the task with provided values
        for field, value in task_update.dict(exclude_unset=True).items():
            setattr(db_task, field, value)

        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

        logger.info(f"Successfully updated task {task_id} for user: {user_id}")

        return db_task

    def delete_task(self, task_id: str, user_id: str) -> bool:
        """
        Delete a specific task by ID for the specified user.
        """
        logger.info(f"Deleting task {task_id} for user: {user_id}")

        task = self.db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            logger.warning(f"Cannot delete task {task_id}: not found for user: {user_id}")
            return False

        self.db_session.delete(task)
        self.db_session.commit()

        logger.info(f"Successfully deleted task {task_id} for user: {user_id}")

        return True

    def toggle_task_completion(self, task_id: str, user_id: str) -> Optional[Task]:
        """
        Toggle the completion status of a specific task.
        """
        logger.info(f"Toggling completion status for task {task_id} for user: {user_id}")

        db_task = self.db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not db_task:
            logger.warning(f"Cannot toggle completion for task {task_id}: not found for user: {user_id}")
            return None

        new_status = not db_task.completed
        db_task.completed = new_status
        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

        logger.info(f"Successfully toggled completion status for task {task_id} for user: {user_id}, new status: {new_status}")

        return db_task