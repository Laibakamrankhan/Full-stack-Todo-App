from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from typing import List
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..services.task_service import TaskService
from ..core.database import get_session
from ..core.security import get_current_user
import logging


router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

# Set up logging
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[TaskRead])
async def get_tasks(
    request: Request,
    completed: bool = None,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the current user.
    Optionally filter by completion status.
    """
    try:
        user_id = current_user["id"]
        logger.info(f"Getting tasks for user: {user_id}, completed filter: {completed}")
        task_service = TaskService(session)
        tasks = task_service.get_tasks_by_user(user_id, completed)
        logger.info(f"Retrieved {len(tasks)} tasks for user: {user_id}")
        return tasks
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {current_user['id']}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving tasks"
        )


@router.post("/", response_model=TaskRead)
async def create_task(
    request: Request,
    task_create: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the current user.
    """
    try:
        user_id = current_user["id"]
        logger.info(f"Creating task for user: {user_id}")

        # Validate input
        if not task_create.title or not task_create.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task title is required"
            )

        task_service = TaskService(session)
        task = task_service.create_task(task_create, user_id)
        logger.info(f"Successfully created task {task.id} for user: {user_id}")
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as they are already handled
        raise
    except Exception as e:
        logger.error(f"Error creating task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the task"
        )


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    request: Request,
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the current user.
    """
    try:
        user_id = current_user["id"]
        logger.info(f"Getting task {task_id} for user: {user_id}")
        task_service = TaskService(session)
        task = task_service.get_task_by_id(task_id, user_id)

        if not task:
            logger.warning(f"Task {task_id} not found for user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Successfully retrieved task {task_id} for user: {user_id}")
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as they are already handled
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {task_id} for user {current_user['id']}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the task"
        )


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    request: Request,
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the current user.
    """
    try:
        user_id = current_user["id"]
        logger.info(f"Updating task {task_id} for user: {user_id}")
        task_service = TaskService(session)
        task = task_service.update_task(task_id, task_update, user_id)

        if not task:
            logger.warning(f"Task {task_id} not found for user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Successfully updated task {task_id} for user: {user_id}")
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as they are already handled
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {current_user['id']}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the task"
        )


@router.delete("/{task_id}")
async def delete_task(
    request: Request,
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the current user.
    """
    try:
        user_id = current_user["id"]
        logger.info(f"Deleting task {task_id} for user: {user_id}")
        task_service = TaskService(session)
        success = task_service.delete_task(task_id, user_id)

        if not success:
            logger.warning(f"Task {task_id} not found for user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Successfully deleted task {task_id} for user: {user_id}")
        return {"message": "Task deleted successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions as they are already handled
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id} for user {current_user['id']}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the task"
        )


@router.patch("/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion(
    request: Request,
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task.
    """
    try:
        user_id = current_user["id"]
        logger.info(f"Toggling completion for task {task_id} for user: {user_id}")
        task_service = TaskService(session)
        task = task_service.toggle_task_completion(task_id, user_id)

        if not task:
            logger.warning(f"Task {task_id} not found for user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Successfully toggled completion for task {task_id} for user: {user_id}")
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as they are already handled
        raise
    except Exception as e:
        logger.error(f"Error toggling task completion {task_id} for user {current_user['id']}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the task"
        )