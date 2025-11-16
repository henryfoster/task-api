
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task_filters import SortOrder, TaskFilters, TaskStatus


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    """
    Repository for Task entity
    handles all database operations
    """

    def get_all_tasks(
        self, page: int, size: int, filters: TaskFilters
    ) -> tuple[list[Task], int]:
        stmt = select(Task)
        # search
        if filters.search:
            stmt = stmt.filter(
                or_(
                    Task.title.ilike(f"%{filters.search}%"),
                    Task.description.ilike(f"%{filters.search}%"),
                )
            )
        # filter
        if filters.status != TaskStatus.ALL:
            completed = filters.status == TaskStatus.COMPLETED
            stmt = stmt.filter(Task.completed == completed)
        # sort
        sort_column = getattr(Task, filters.sort_by)
        if filters.sort_order == SortOrder.DESC:
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column.asc())

        offset = (page - 1) * size
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        result = self.db.execute(stmt.offset(offset).limit(size))
        items = result.scalars().all()
        return list(items), total

    def get_task_by_id(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def create_task(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
