from unittest.mock import Mock

from app.models.task import Task
from app.schemas.task import TaskCreate
from app.services.task_service import TaskService


def test_create_task() -> None:
    mock_repo = Mock()
    mock_repo.create_task.return_value = Task(
        id=1, title="Test", description="desc", completed=False
    )

    service = TaskService(mock_repo)

    task_data = TaskCreate(title="Test", description="desc")
    result = service.create_task(task_data)

    mock_repo.create_task.assert_called_once()
    call_args = mock_repo.create_task.call_args[0][0]  # First argument of first call
    assert isinstance(call_args, Task)
    assert call_args.title == "Test"
    assert call_args.description == "desc"
    assert not call_args.completed

    assert result.title == "Test"
