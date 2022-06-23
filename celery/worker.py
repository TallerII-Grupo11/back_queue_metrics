import os
from celery import Celery
import redis

CELERY_BROKER_URL = os.getenv("BROKER")
CELERY_RESULT_BACKEND = os.getenv("BROKER")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASS = os.getenv("REDIS_PASS")

celery = Celery("celery", backend=CELERY_BROKER_URL, broker=CELERY_RESULT_BACKEND)

red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASS)

