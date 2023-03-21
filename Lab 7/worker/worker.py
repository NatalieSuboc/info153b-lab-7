import os
import time
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

broker_url = os.environ.get("CELERY_BROKER_URL")
res_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery_app = Celery(name='worker', broker=broker_url, result_backend=res_backend)

@celery_app.task
def count_word_task(text):
    # perform task
    length = len(text.split(' '))
    time.sleep(length)
    return length
    