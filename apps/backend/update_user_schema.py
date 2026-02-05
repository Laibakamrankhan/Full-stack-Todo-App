import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlmodel import create_engine
from src.core.config import settings
from sqlalchemy import text

def update_user_table_schema():
    """Update user table schema to include name field."""
    engine = create_engine(settings.database_url)

    with engine.connect() as conn:
        # Check if name column exists in the user table
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'user' AND column_name = 'name'
        """)).fetchall()

        if not result:
            print("Adding name column to user table...")
            # Add name column to user table (allowing NULL initially)
            conn.execute(text("ALTER TABLE \"user\" ADD COLUMN name TEXT"))
            conn.commit()
            print("Name column added successfully!")
        else:
            print("Name column already exists")

        # Also check if hashed_password exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'user' AND column_name = 'hashed_password'
        """)).fetchall()

        if not result:
            print("Adding hashed_password column to user table...")
            conn.execute(text("ALTER TABLE \"user\" ADD COLUMN hashed_password TEXT NOT NULL DEFAULT ''"))
            conn.execute(text("UPDATE \"user\" SET hashed_password = '' WHERE hashed_password IS NULL"))
            conn.commit()
            print("Hashed password column added successfully!")

    print("User table schema update completed!")

if __name__ == "__main__":
    update_user_table_schema()