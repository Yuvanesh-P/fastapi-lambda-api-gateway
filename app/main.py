from fastapi import FastAPI, HTTPException
from mangum import Mangum

from app.models import TaskCreate, TaskUpdate

app = FastAPI(
    title="FastAPI Lambda API",
    description="FastAPI deployed using AWS Lambda and API Gateway",
    version="1.0.0"
)

# In-memory storage for demonstration only.
# Data will not persist across Lambda execution environments.
tasks = {}
task_counter = 1


@app.get("/")
def home():
    return {
        "message": "FastAPI running on AWS Lambda",
        "status": "healthy"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global task_counter

    task_id = task_counter

    tasks[task_id] = {
        "id": task_id,
        **task.model_dump()
    }

    task_counter += 1

    return tasks[task_id]


@app.get("/tasks")
def get_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    return tasks[task_id]


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks[task_id].update(task.model_dump())

    return tasks[task_id]


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks[task_id]

    return {"message": "Task deleted successfully"}


# AWS Lambda entry point
handler = Mangum(app)