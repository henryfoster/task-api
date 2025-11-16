# configuration and fixtures
from typing import Any, Callable, Generator, Optional

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.task import Task

# SQLite in-memory database for testing
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

# Create test engine with special settings for SQLite
test_engine = create_engine(
    SQLALCHEMY_TEST_URL,
    poolclass=StaticPool,  # Keep connection alive for in-memory DB
    connect_args={"check_same_thread": False},  # Allow multiple threads
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Override the database dependency
def override_get_db() -> Generator:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture  # (scope="session")
def setup_test_db() -> Generator[None, Any, None]:
    """Create database tables once for all tests"""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(
    setup_test_db: Generator[None, Any, None],
) -> Generator[TestClient, None, None]:
    # Tables already exist from setup_test_db
    app.dependency_overrides[get_db] = override_get_db  # type: ignore
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()  # type: ignore


@pytest.fixture
def sample_tasks(setup_test_db: Generator[None, Any, None]) -> list[Task]:
    # Tables already exist from setup_test_db
    db = TestSessionLocal()
    try:
        db.query(Task).delete()
        tasks = [
            Task(title="Task1", description="Description 1", completed=False),
            Task(title="Task2", description="Description 2", completed=True),
            Task(title="Task3", description="Description 3", completed=False),
            Task(title="Task4", description="Description 4", completed=True),
            Task(title="Task5", description="Description 5", completed=False),
            Task(title="Task6", description="Description 6", completed=True),
            Task(title="Task7", description="Description 7", completed=False),
            Task(title="Task8", description="Description 8", completed=False),
            Task(title="Task9", description="Description 9", completed=False),
            Task(title="Task10", description="Description 10", completed=False),
            Task(title="Search Me", description="Find this task", completed=False),
            Task(title="Another One", description="More content", completed=True),
            Task(title="Test Task", description="Testing search", completed=False),
        ]
        for task in tasks:
            db.add(task)
        db.commit()
        return tasks
    finally:
        db.close()


@pytest.fixture
def task_factory(
    setup_test_db: Generator[None, Any, None],
) -> Callable[[str, Optional[str], bool], Task]:
    def _create_task(
        title: str = "Test Task",
        description: Optional[str] = "Task Description",
        completed: bool = False,
    ) -> Task:
        db = TestSessionLocal()
        try:
            task = Task(title=title, description=description, completed=completed)
            db.add(task)
            db.commit()
            db.refresh(task)
            return task
        finally:
            db.close()

    return _create_task
