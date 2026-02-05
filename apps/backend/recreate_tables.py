import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import SQLModel, create_engine
from sqlalchemy import text
from src.core.config import settings
from src.models.user import User
from src.models.task import Task

def recreate_tables():
    """Drop and recreate all tables to ensure schema matches the model."""
    engine = create_engine(settings.database_url)

    print("Dropping and recreating all tables...")

    # Reflect existing tables and drop them
    with engine.connect() as conn:
        # Get all table names
        result = conn.execute(text("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
        """)).fetchall()

        table_names = [row[0] for row in result]
        print(f"Existing tables: {table_names}")

        # Drop all existing tables
        for table_name in table_names:
            if table_name in ['user', 'task']:  # Only drop our tables
                print(f"Dropping table: {table_name}")
                conn.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))

        conn.commit()

    # Now recreate using SQLModel
    SQLModel.metadata.create_all(engine)
    print("Tables recreated successfully!")

if __name__ == "__main__":
    recreate_tables()