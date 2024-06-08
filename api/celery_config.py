broker_url = 'redis://localhost:6379/0'
result_backend = 'db+sqlite:///results.db'
broker_connection_retry_on_startup = True
imports = (
  'api.v1.helpers.tasks.celery_tasks',
  'api.v1.helpers.tasks.attendance_tasks',
  'api.v1.helpers.tasks.mail_tasks',
)

config = {
    'broker_url': broker_url,
    'result_backend': result_backend,
    'broker_connection_retry_on_startup': broker_connection_retry_on_startup,
    'imports': imports,
}
