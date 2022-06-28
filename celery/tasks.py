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
        total = red.hincrby("songs", "quantity", 1)
        genre_q = red.hincrby("songs.genre", f"{genre}", 1)
        list_artist = []
        for art in artists:
            artist_id = art['artist_id']
            artist_count = red.hincrby(f"user.{artist_id}", "songs", 1)
            list_artist.append({artist_id: artist_count})

        return {"result": f"New song",
                "total_songs": total,
                "artist_songs": list_artist,
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

@celery.task(name='new.album')
def new_album(subscription, artists):
    try:
        artist_id = artists['artist_id']
        total = red.hincrby("albums", "quantity", 1)
        subscription_count = red.hincrby("subscription", f"{subscription}", 1)
        artist = red.hincrby(f"user.{artist_id}", "albums", 1)
        
        return {
            "result": f"New song",
            "total_albums": total,
            "artist_albums": artist,
            "subscription": {subscription: subscription_count}
        }
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex



@celery.task(name='new.playlist')
def new_playlist(user_id):
    try:
        total = red.hincrby("playlists", "quantity", 1)
        listener = red.hincrby(f"user.{user_id}", "playlists", 1)

        return {
            "result": f"New song",
            "total_playlists": total,
            "listener_playlist": listener,
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
