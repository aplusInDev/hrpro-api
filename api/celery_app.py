from celery import Celery
from api.celery_config import config

## to start celery app
## celery -A api.celery_app worker -l info

celery_app = Celery('celery_app')
celery_app.config_from_object(config)
