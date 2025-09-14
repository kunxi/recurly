from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import create_engine as sa_create_engine
import os

# Database URL - you can change this to PostgreSQL or MySQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recurly.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session
