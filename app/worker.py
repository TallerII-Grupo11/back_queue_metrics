import os
from celery import Celery

CELERY_BROKER_URL = os.getenv("BROKER")
CELERY_RESULT_BACKEND = os.getenv("BROKER")

celery = Celery("celery", backend=CELERY_BROKER_URL, broker=CELERY_RESULT_BACKEND)
