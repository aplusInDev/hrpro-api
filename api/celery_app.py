from celery import Celery
from api.celery_config import config

# to start celery app
# celery -A api.celery_app worker -l info

app = Celery('celery_app')
app.config_from_object(config)
