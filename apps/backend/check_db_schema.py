import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from src.core.config import settings

def check_user_table_structure():
    """Check the current structure of the user table."""
    engine = create_engine(settings.database_url)

    with engine.connect() as conn:
        # Check all columns in the user table
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'user'
            ORDER BY ordinal_position
        """)).fetchall()

        print("Current structure of 'user' table:")
        for row in result:
            print(f"  {row[0]}: {row[1]}, nullable={row[2]}, default={row[3]}")

        print("\nChecking for existing users:")
        count_result = conn.execute(text("SELECT COUNT(*) FROM \"user\"")).fetchone()
        print(f"Total users in table: {count_result[0]}")

        print("\nChecking for any existing user with the problematic email:")
        try:
            existing_result = conn.execute(text("SELECT id, email, name FROM \"user\" WHERE email = 'minha123@gmail.com'")).fetchall()
            if existing_result:
                print(f"Found existing user: {existing_result}")
            else:
                print("No existing user found with that email")
        except Exception as e:
            print(f"Could not check for existing user: {e}")

        # Check table constraints
        print("\nChecking constraints on user table:")
        constraint_result = conn.execute(text("""
            SELECT tc.constraint_name, tc.constraint_type, kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = 'user'
            ORDER BY tc.constraint_name, kcu.ordinal_position
        """)).fetchall()

        for constraint in constraint_result:
            print(f"  {constraint[0]}: {constraint[1]} on {constraint[2]}")

if __name__ == "__main__":
    check_user_table_structure()