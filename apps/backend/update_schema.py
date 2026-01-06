import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlmodel import SQLModel, create_engine, text
from src.core.config import settings
from src.models.task import Task

def update_database_schema():
    """Update database schema to include category field."""
    engine = create_engine(settings.database_url)

    # Check if category column exists in the task table
    with engine.connect() as conn:
        # Check existing columns in task table
        result = conn.execute(text("PRAGMA table_info(task)")).fetchall()
        columns = [row[1] for row in result]  # Column name is at index 1

        print(f"Existing columns in task table: {columns}")

        # Add category column if it doesn't exist
        if 'category' not in columns:
            print("Adding category column to task table...")
            conn.execute(text("ALTER TABLE task ADD COLUMN category TEXT DEFAULT 'General'"))
            conn.commit()
            print("Category column added successfully!")
        else:
            print("Category column already exists")

    print("Database schema update completed!")

if __name__ == "__main__":
    update_database_schema()