class TaskNotFoundException(Exception):
    def __init__(self, task_id: int):
        super().__init__(f"Task with id {task_id} not found")
