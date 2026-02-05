import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import SQLModel, create_engine
from sqlalchemy import text
from src.core.config import settings
from src.models.user import User

def sync_database_schema():
    """Sync the database schema with the model definition."""
    engine = create_engine(settings.database_url)

    print("Syncing database schema...")

    # Let's check what tables exist first
    with engine.connect() as conn:
        # Check current columns
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'user'
            ORDER BY ordinal_position
        """)).fetchall()

        print(f"\nCurrent columns in database: {[row[0] for row in result]}")

        # According to our model, we need these columns:
        # id, email, name, hashed_password, created_at, updated_at
        expected_columns = {'id', 'email', 'name', 'hashed_password', 'created_at', 'updated_at'}
        actual_columns = {row[0] for row in result}

        print(f"Expected columns: {expected_columns}")
        print(f"Actual columns: {actual_columns}")

        # Find missing columns
        missing_columns = expected_columns - actual_columns
        extra_columns = actual_columns - expected_columns

        print(f"Missing columns: {missing_columns}")
        print(f"Extra columns: {extra_columns}")

        # Add missing columns if any
        for col in missing_columns:
            if col == 'name':
                conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS name TEXT'))
            elif col == 'hashed_password':
                conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS hashed_password VARCHAR NOT NULL DEFAULT \'\''))
            elif col == 'created_at':
                conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW()'))
            elif col == 'updated_at':
                conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW()'))
            elif col == 'email':
                conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email VARCHAR UNIQUE NOT NULL'))

        # Update the email column to have a unique constraint if it doesn't have one
        # Check for existing unique constraints on email
        constraint_check = conn.execute(text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'user'
            AND constraint_type = 'UNIQUE'
            AND constraint_name LIKE '%email%'
        """)).fetchall()

        if not constraint_check:
            print("Adding unique constraint to email column...")
            try:
                conn.execute(text('ALTER TABLE "user" ADD CONSTRAINT user_email_unique UNIQUE (email)'))
            except Exception as e:
                print(f"Could not add unique constraint (might already exist): {e}")

        # Check for primary key constraint
        pk_check = conn.execute(text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'user'
            AND constraint_type = 'PRIMARY KEY'
        """)).fetchall()

        if not pk_check:
            print("Adding primary key constraint to id column...")
            try:
                conn.execute(text('ALTER TABLE "user" ADD CONSTRAINT user_pkey PRIMARY KEY (id)'))
            except Exception as e:
                print(f"Could not add primary key constraint (might already exist): {e}")

        conn.commit()

        print("Database schema sync completed!")

if __name__ == "__main__":
    sync_database_schema()