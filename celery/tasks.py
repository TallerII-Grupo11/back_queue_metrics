from time import sleep
from logging import getLogger
import traceback

from metric_name import *
from celery import current_task, states
from celery.exceptions import Ignore

from worker import celery, red

LOGGER = getLogger(__name__)



@celery.task(name='new.register')
def user_register():
    try:
        total = red.hincrby("new.register", "quantity", 1)
        return {"result": f"New user register",
                "total": f"{total}"}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex


@celery.task(name='new.login')
def user_login():
    try:
        total = red.hincrby("new.login", "quantity", 1)

        return {"result": f"New user login",
                "total": f"{total}"}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex


@celery.task(name='new.song')
def new_song(artists, genre):
    try:
        total = red.hincrby("song", "quantity", 1)
        genre_q = red.hincrby("song.genre", f"{genre}", 1)
        list_artist = []
        for art in artists:
            artist_id = art['artist_id']
            artist_count = red.hincrby("song.artist", artist_id, 1)
            list_artist.append({artist_id: artist_count})

        return {"result": f"New song",
                "total": total,
                "artist": list_artist,
                "genre": {genre: genre_q}
        }
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex



@celery.task(name='delete.all', bind=True, acks_late=True)
def delete_metrics():
    try:
        for metric in get_all_metrics():
            red.delete(metric)
        
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex
