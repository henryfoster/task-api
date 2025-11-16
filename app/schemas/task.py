from datetime import datetime
from typing import ClassVar, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskBase(BaseModel):
    TITLE_MIN_LENGTH: ClassVar[int] = 3
    TITLE_MAX_LENGTH: ClassVar[int] = 255
    DESCRIPTION_MAX_LENGTH: ClassVar[int] = 1000


class TaskCreate(TaskBase):
    title: str = Field(
        min_length=TaskBase.TITLE_MIN_LENGTH, max_length=TaskBase.TITLE_MAX_LENGTH
    )
    description: Optional[str] = Field(None, max_length=TaskBase.DESCRIPTION_MAX_LENGTH)

    @field_validator("title")
    @classmethod
    def validate_title(cls, task_title: str) -> str:
        cleaned_title = task_title.strip()
        if not cleaned_title:
            raise ValueError("title can't be empty")
        return cleaned_title


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(TaskBase):
    title: Optional[str] = Field(
        None, min_length=TaskBase.TITLE_MIN_LENGTH, max_length=TaskBase.TITLE_MAX_LENGTH
    )
    description: Optional[str] = Field(None, max_length=TaskBase.DESCRIPTION_MAX_LENGTH)
    completed: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, task_title: str | None) -> str | None:
        if task_title is None:  # Handle optional fields
            return task_title
        cleaned_title = task_title.strip()
        if not cleaned_title:
            raise ValueError("title can't be empty")
        return cleaned_title
