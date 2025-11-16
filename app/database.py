import os
from typing import Any, Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
assert DATABASE_URL is not None, "DATABASE_URL environment variable is required"


engine = create_engine(
    DATABASE_URL
)  # Database connection object (similar to Doctrine's connection
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  #  Creates database sessions (like Doctrine's EntityManager)
Base = (
    declarative_base()
)  # Base class your models will inherit from (like Symfony Entity base)


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
