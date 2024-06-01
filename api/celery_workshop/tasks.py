from celery import Celery
from time import sleep

app = Celery('tasks')
app.config_from_object('celery_config')

@app.task
def send_email(email_address, subject, message):
    """Send an email to the given email address with the given subject and message."""
    sleep(20)
    # Simulate sending an email
    print(f"Sending email to ({email_address}) with subject ({subject})")
    # Replace with actual email sending logic
    return f"Email sent to ({email_address}) with subject ({subject}) and message ({message})"
