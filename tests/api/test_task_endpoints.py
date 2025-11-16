from fastapi.testclient import TestClient

from app.models.task import Task


def test_get_tasks_empty(client: TestClient) -> None:
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["size"] == 10
    assert data["pagination"]["total"] == 0
    assert data["pagination"]["pages"] == 0
    assert not data["pagination"]["has_next"]
    assert not data["pagination"]["has_prev"]

def test_get_tasks_with_sample_data(
    client: TestClient, sample_tasks: list[Task]
) -> None:
    response = client.get("/tasks")
    data = response.json()
    assert len(data["items"]) == 10
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["size"] == 10
    assert data["pagination"]["total"] == 13
    assert data["pagination"]["pages"] == 2
    assert data["pagination"]["has_next"]
    assert not data["pagination"]["has_prev"]


def test_get_tasks_with_search(client: TestClient, sample_tasks: list[Task]) -> None:
    response = client.get("/tasks?search=Task2")
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Task2"
