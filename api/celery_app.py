from celery import Celery
from api.celery_config import config

app = Celery('celery_app')
app.config_from_object(config)
