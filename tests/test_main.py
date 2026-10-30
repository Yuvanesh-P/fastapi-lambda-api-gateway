from fastapi.testclient import TestClient
from app import main

client = TestClient(main.app)


def setup_function():
    main.tasks.clear()
    main.task_counter = 1


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Learn AWS Lambda",
            "description": "Deploy FastAPI",
            "completed": False
        }
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_get_tasks():
    client.post(
        "/tasks",
        json={
            "title": "Learn Terraform",
            "description": "Create infrastructure",
            "completed": False
        }
    )

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_task():
    client.post(
        "/tasks",
        json={
            "title": "Test task",
            "description": "Delete task",
            "completed": False
        }
    )

    response = client.delete("/tasks/1")
    assert response.status_code == 200