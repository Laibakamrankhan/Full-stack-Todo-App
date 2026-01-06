import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlmodel import SQLModel
from src.core.database import engine
from src.models.user import User
from src.models.task import Task

def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_db_and_tables()