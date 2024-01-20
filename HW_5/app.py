'''Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание. Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку Pydantic.'''

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class TaskBase(BaseModel):
    title: str
    description: str
    status: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int

tasks_db = []
task_id_counter = 1

# Получение списка всех задач
@app.get("/tasks", response_model=List[Task])
def read_tasks():
    return tasks_db

# Получение задачи по идентификатору
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int = Path(..., title="The ID of the task")):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Добавление новой задачи
@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    global task_id_counter
    new_task = Task(id=task_id_counter, **task.dict())
    task_id_counter += 1
    tasks_db.append(new_task)
    return new_task

# Обновление задачи по идентификатору
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    existing_task = next((t for t in tasks_db if t["id"] == task_id), None)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    existing_task.update(**task.dict())
    return existing_task

# Удаление задачи по идентификатору
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    task_index = next((index for index, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    deleted_task = tasks_db.pop(task_index)
    return deleted_task
