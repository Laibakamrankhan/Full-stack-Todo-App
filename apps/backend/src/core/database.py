from sqlmodel import create_engine, Session
from .config import settings

# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=True,  # Set to False in production
    pool_pre_ping=True,
    pool_recycle=300,
)


def get_session():
    with Session(engine) as session:
        yield session