from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    category: str = "General"  # Default category


class Task(TaskBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)  # Foreign key reference to user
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    category: Optional[str] = None