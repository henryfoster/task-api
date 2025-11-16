from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_task_filters, get_task_service
from app.exceptions.TaskNotFoundException import TaskNotFoundException
from app.models.task import Task
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.task_filters import TaskFilters
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
def get_all_tasks(
    pagination_params: PaginationParams = Depends(),
    task_filters: TaskFilters = Depends(get_task_filters),
    task_service: TaskService = Depends(get_task_service),
) -> PaginatedResponse[TaskResponse]:
    return task_service.get_paginated_tasks(pagination_params, task_filters)


@router.get("/{task_id}", response_model=TaskResponse)
def get_single_task(
    task_id: int, task_service: TaskService = Depends(get_task_service)
) -> Task:
    task = task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_data: TaskCreate, task_service: TaskService = Depends(get_task_service)
) -> Task:
    return task_service.create_task(task_data)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
) -> Task:
    try:
        task = task_service.update_task(task_id, task_data)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, task_service: TaskService = Depends(get_task_service)
) -> None:
    try:
        task_service.delete_task(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
