from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict
from uuid import UUID, uuid4
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import time
from collections import defaultdict

from starlette.responses import Response

app = FastAPI()

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        print("*****Inside 333333 RateLimiterMiddleware init- Begin ")
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)
        print("*****Inside 333333 RateLimiterMiddleware init- End ")


    async def log_message(self, message:str):
        print(message)


    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        print("*****Inside 333333 RateLimiterMiddleware dispatch- Begin ")
        client_ip = request.client.host
        current_time = time.time()
        if current_time - self.rate_limit_records[client_ip] < 1 : #1 request per second
            return Response(content="Rate Limit Exceeded" , status_code=429)

        self.rate_limit_records[client_ip] = current_time
        path = request.url.path
        await self.log_message(f"Request to path = {path}")

        #Process Request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        #add Custom Header
        custom_header = {"X-PROCESS-TIME": str(process_time)}
        for key, value in custom_header.items():
            response.headers.append(key, value)

        await self.log_message(f"Request to path = {path} took {process_time} seconds")
        print("*****Inside 333333 RateLimiterMiddleware dispatch- End ")
        return response

#add middleware to app
app.add_middleware(RateLimiterMiddleware)

class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks = []

@app.middleware("http")
async def response_id_header(request: Request, call_next):
    print("*****Inside 111111 response_id_header - Begin ")
    response = await call_next(request)
    response.headers["X-RESPONSE-ID"]="some_header"
    print("*****Inside 111111 response_id_header - End ")
    return response

@app.middleware("http")
async def response_checker(request: Request, call_next):
    print("*****Inside 222222 response_checker - Begin ")
    response = await call_next(request)
    response.headers["X-RESPONSE-ID2"]="some_header2"
    print("*****Inside 222222 response_checker - End ")
    return response

@app.get("/")
def index():
    print("*****Inside API - Begin")
    data = {"hello" : "world"}
    print("*****Inside API - End")
    return data

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
