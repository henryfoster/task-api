
from app.exceptions.TaskNotFoundException import TaskNotFoundException
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.task_filters import TaskFilters
from app.services.pagination_factory import PaginationFactory


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def get_paginated_tasks(
        self, pagination_params: PaginationParams, filters: TaskFilters
    ) -> PaginatedResponse[TaskResponse]:
        tasks, total = self.task_repository.get_all_tasks(
            pagination_params.page, pagination_params.size, filters
        )
        meta = PaginationFactory.create_pagination_meta(
            page=pagination_params.page, size=pagination_params.size, total=total
        )
        task_responses = [TaskResponse.model_validate(task) for task in tasks]
        return PaginatedResponse(items=task_responses, pagination=meta)

    def get_task_by_id(self, task_id: int) -> Task | None:
        return self.task_repository.get_task_by_id(task_id)

    def create_task(self, task_data: TaskCreate) -> Task:
        new_task = Task(
            title=task_data.title, description=task_data.description, completed=False
        )
        return self.task_repository.create_task(new_task)

    def update_task(self, task_id: int, task_update_dto: TaskUpdate) -> Task:
        task_to_update = self.task_repository.get_task_by_id(task_id)
        if task_to_update is None:
            raise TaskNotFoundException(task_id)
        update_data = task_update_dto.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(task_to_update, field):
                setattr(task_to_update, field, value)
        updated_task = self.task_repository.update_task(task_to_update)
        return updated_task

    def delete_task(self, task_id: int) -> None:
        task = self.task_repository.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundException(task_id)
        self.task_repository.delete_task(task)
