"""
The db module contains the setup of the database connection.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DB URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# The BaseDeclarativeClass is the base model to declare all tables
class BaseDeclarativeClass(DeclarativeBase):
    pass


def get_db():
    """Creates a connection to the database."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()