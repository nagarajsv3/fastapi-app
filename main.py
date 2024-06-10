from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks = []

@app.get("/")
def index():
    return {"hello" : "world"}

@app.get("/tasks", response_model=List[Task])
def read_tasks():
    return tasks

@app.get("/task/{task_id}", response_model=Task)
def read_task(task_id : UUID):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task Not Found")

@app.put("/task/{task_id}", response_model=Task)
def update_task(task_id : UUID, updatedtask:Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            newtask = task.copy(update=updatedtask.dict(exclude_unset=True))
            tasks[idx] = newtask
            return newtask

    raise HTTPException(status_code=404, detail="Task Not Found")

@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id : UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(idx)

    raise HTTPException(status_code=404, detail="Task Not Found")

@app.post("/task", response_model=Task)
def create_task(task : Task):
    task.id = uuid4()
    tasks.append(task)
    return task

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
