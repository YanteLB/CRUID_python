
from fastapi import FastAPI, HTTPException

app = FastAPI()



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

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task
#def main():
 #   print("Hello from cruid-python!")


#if __name__ == "__main__":
#    main()
