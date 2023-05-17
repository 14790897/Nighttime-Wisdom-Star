# celery_config.py
from celery import Celery

app = Celery('myapp', broker='redis://localhost:6379/0')
