import os
import json
from pydantic import BaseModel
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from worker import celery
from metric_name import *
from model import User, Task 

title = os.getenv("TITLE")

app = FastAPI(title=title)


@app.post("/login")
async def new_login(user: User,  federated: bool = None):
    task_name = metric_login(federated)
    task = celery.send_task(task_name, args=[user.id])
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_202_ACCEPTED
    )


@app.post("/register")
async def new_register(user: User, federated: bool = None):
    task_name = metric_register(federated)
    task = celery.send_task(task_name, args=[user.id])
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_202_ACCEPTED
    )
    #return dict(task_id=task.id)


@app.get("/check_task/{id}")
def check_task(id: str):
    task = celery.AsyncResult(id)
    if task.state == 'SUCCESS':
        response = {
            'status': task.state,
            'result': task.result,
            'task_id': id
        }
    elif task.state == 'FAILURE':
        response = json.loads(task.backend.get(task.backend.get_key_for_task(task.id)).decode('utf-8'))
        del response['children']
        del response['traceback']
    else:
        response = {
            'status': task.state,
            'result': task.info,
            'task_id': id
        }
    return JSONResponse(
        content=response,
        status_code=status.HTTP_200_OK
    )
