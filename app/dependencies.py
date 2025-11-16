from typing import Optional

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.task_repository import TaskRepository
from app.schemas.task_filters import SortBy, SortOrder, TaskFilters, TaskStatus
from app.services.task_service import TaskService


def get_task_filters(
    search: Optional[str] = Query(
        None, max_length=100, description="Search in title and description"
    ),
    status: TaskStatus = Query(
        TaskStatus.ALL, description="Filter by completion status"
    ),
    sort_by: SortBy = Query(SortBy.CREATED_AT, description="Sort field"),
    sort_order: SortOrder = Query(SortOrder.DESC, description="Sort direction"),
) -> TaskFilters:
    return TaskFilters(
        search=search, status=status, sort_by=sort_by, sort_order=sort_order
    )


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


def get_task_service(
    task_repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(task_repository=task_repository)
