import os
import json
import time
from pydantic import BaseModel
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from worker import celery
from metric_name import *
from model import *
from logging import getLogger
from redis_connection import RedisConnection

title = os.getenv("TITLE")
port = os.getenv("PORT")

app = FastAPI(title=title)

LOGGER = getLogger(__name__)


@app.post("/login")
async def new_login(federated: bool = None):
    task_name = "new.login"
    task = celery.send_task(task_name)
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_202_ACCEPTED
    )


@app.post("/users")
async def new_register(federated: bool = None):
    task_name = "new.register"
    task = celery.send_task(task_name)
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_202_ACCEPTED
    )

@app.post("/blocked")
async def user_blocked():
    task_name = "user.block"
    task = celery.send_task(task_name)
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_202_ACCEPTED
    )


@app.post("/password_reset")
async def password_reset():
    task_name = "password.reset"
    task = celery.send_task(task_name)
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_202_ACCEPTED
    )


@app.post("/song")
async def new_register(song: Song):
    task_name = "new.song"
    artists = song.get_artists()
    task = celery.send_task(task_name, args=[artists, song.genre])
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_202_ACCEPTED
    )


@app.post("/album")
async def new_register(album: Album):
    task_name = "new.album"
    task = celery.send_task(task_name, args=[album.subscription, album.artist.dict(), album.genre])
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_202_ACCEPTED
    )


@app.post("/playlist")
async def new_register(playlist: Playlist):
    task_name = "new.playlist"
    task = celery.send_task(task_name, args=[playlist.owner_id])
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_202_ACCEPTED
    )


@app.get("/metrics")
async def register_result():
    try:
        results = RedisConnection().get_all_metrics()
        return results
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


@app.delete("/metrics", include_in_schema=False)
async def register_result(federated: bool = None):
    task_name = "delete.all"
    task = celery.send_task(task_name)
    return JSONResponse(
        content={"id": task.id, "name": task_name},
        status_code=status.HTTP_200_OK
    )


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=port,  reload=True)