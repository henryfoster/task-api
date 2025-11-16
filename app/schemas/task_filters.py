from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    ALL = "all"


class SortBy(str, Enum):
    CREATED_AT = "created_at"
    TITLE = "title"
    STATUS = "completed"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class TaskFilters(BaseModel):
    search: Optional[str] = Field(
        None, max_length=100, description="Search in title and description"
    )
    status: str = Field(TaskStatus.ALL, description="Filter by completion status")
    sort_by: str = Field(SortBy.CREATED_AT, description="Sort by")
    sort_order: str = Field(SortOrder.DESC, description="Sort direction")
