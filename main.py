
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
app = FastAPI()

#validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        field = error["loc"][-1]
        if error["type"] == "missing":
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"error": f"Field '{field}' is required."},
            )
        if error["type"] == "extra_forbidden":
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"error": f"Unknown field '{field}'. Check for typos."},
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )



tasks:list[dict] = [
    {"id": 1, "title": "Task 1", "description": "This is task 1", "completed": False},
    {"id": 2, "title": "Task 2", "description": "This is task 2", "completed": True},
    {"id": 3, "title": "Task 3", "description": "This is task 3", "completed": False},
]


@app.get("/")
def root():
    return {"name":"Task API", "version":"1", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Task {task_id} not found"})
    return task

class Task(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    model_config = {"extra": "forbid"}
    title: str | None = None
    completed: bool | None = None
    description: str | None = None



@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    task_id = max((task["id"] for task in tasks), default=0) + 1 if tasks else 1
    title = task.title
    if title is None or title.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required")
    new_task = {"id": task_id, "title": title+f"{task_id}", "description": f"This is task {task_id}", "completed": False}
    tasks.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def patch_task(task_id: int, task: TaskUpdate):
    if not task or (task.title is None and task.completed is None and task.description is None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    existing_task = next((t for t in tasks if t["id"] == task_id), None)
    if existing_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Task {task_id} not found"})
    if task.title is not None:
        if task.title.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty") 
        existing_task["title"] = task.title
    if task.completed is not None:
        if not isinstance(task.completed, bool):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Completed must be a boolean value")
        existing_task["completed"] = task.completed
    if task.description is not None:
        if task.description.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Description cannot be empty")
        existing_task["description"] = task.description
    return existing_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    existing_task = next((t for t in tasks if t["id"] == task_id), None)
    if existing_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Task {task_id} not found"})
    tasks.remove(existing_task)

