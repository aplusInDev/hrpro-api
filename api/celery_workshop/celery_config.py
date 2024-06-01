# celery_config.py
broker_url = 'redis://localhost:6379/0'
result_backend = 'db+sqlite:///results.db'
broker_connection_retry_on_startup = True
