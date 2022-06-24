import os
import json
import time
from pydantic import BaseModel
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from worker import celery
from metric_name import *
from model import User
from logging import getLogger
from redis_connection import RedisConnection

title = os.getenv("TITLE")
port = os.getenv("PORT")

app = FastAPI(title=title)

LOGGER = getLogger(__name__)


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

@app.get("/metrics")
async def register_result(federated: bool = None):
    try:
        metrics = get_metrics()
        results = RedisConnection().get_all_metrics(metrics)
        return JSONResponse(
        content=results,
        status_code=status.HTTP_200_OK
    )
    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=f"Could not get metrics results. Exception: {ex}"
        )


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


@app.delete("/metrics") # , include_in_schema=False
async def register_result(federated: bool = None):
    task_name = "delete.all"
    task = celery.send_task(task_name)
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_200_OK
    )


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=port,  reload=True)