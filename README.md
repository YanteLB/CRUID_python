# Task API

A simple CRUD REST API built with **FastAPI** and **Python 3.12**. It manages a list of tasks in memory — create, read, update, and delete tasks via HTTP.

---

## Install & Run

```bash
uv run fastapi dev main.py
```

> This installs dependencies (via `uv`) and starts the development server at `http://localhost:8000`.  
> Hot-reload is enabled — the server restarts automatically on file changes.

---

## Endpoints

| Method | Path | Status | Description |
|--------|------|--------|-------------|
| `GET` | `/` | 200 | API info |
| `GET` | `/health` | 200 | Health check |
| `GET` | `/tasks` | 200 | List all tasks |
| `GET` | `/tasks/:id` | 200 / 404 | Get a single task |
| `POST` | `/tasks` | 201 / 422 | Create a new task |
| `PATCH` | `/tasks/:id` | 200 / 400 / 404 | Partially update a task |
| `DELETE` | `/tasks/:id` | 204 / 404 | Delete a task |

---

## Example `curl -i` Output

```
$ curl -i -X POST localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'

HTTP/1.1 201 Created
content-type: application/json
content-length: 81

{"id":4,"title":"Buy groceries4","description":"This is task 4","completed":false}
```

---

## Swagger UI

FastAPI generates interactive docs automatically. Open your browser at:

```
http://localhost:8000/docs
```

Add your Swagger screenshot here:

![Swagger UI](swagger.png)
