from itertools import count

import uvicorn
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Простой CRUD")


class TaskInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=200)


class Task(TaskInput):
    id: int


# Данные для демонстрации: после перезапуска сервера записи исчезнут.
tasks: dict[int, Task] = {}
task_ids = count(1)

@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return tasks[task_id]


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(data: TaskInput):
    task = Task(id=next(task_ids), title=data.title)
    tasks[task.id] = task
    return task


@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskInput):
    get_task(task_id)
    tasks[task_id] = Task(id=task_id, title=data.title)
    return tasks[task_id]


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    get_task(task_id)
    del tasks[task_id]
    return Response(status_code=204)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


