from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "sqlmodel>=0.0.16",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "asyncpg>=0.29.0",
        "psycopg2-binary>=2.9.9",
        "alembic>=1.13.1",
        "sqlalchemy>=2.0.23",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.11",
)