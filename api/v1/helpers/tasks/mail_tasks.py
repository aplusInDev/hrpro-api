from flask_mail import Message
from os import getenv
from api.celery_app import app
from flask import render_template


@app.task
def send_welcome_mail_task(name, email, password):
    """Celery task to send welcome email."""
    from api.v1.app import create_app, mail
    app = create_app()  # Create an instance of our Flask app
    with app.app_context():  # Push the application context
        # we use app_context to have access to the application context
        # because we are outside the application context
        try:
            data = {
                "name": name,
                "email": email,
                "password": password,
                "login_link": "http://localhost:3000/login"
            }
            msg = Message("Welcome to HRPro", sender=getenv('HRPRO_EMAIL'),
                        recipients=[email])
            msg.html = render_template("email_welcome.html", data=data)
            mail.send(msg)
            return "task done successfully"
        except Exception as err:
            return "task failed" + str(err)
