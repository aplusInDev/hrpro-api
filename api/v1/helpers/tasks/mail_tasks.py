from flask_mail import Message
from os import getenv
from api.celery_app import celery_app
from flask import render_template
from api.v1.auth.auth import SessionAuth
from api.v1.auth import db


@celery_app.task
def send_welcome_mail_task(name, email, password) -> str:
    """Celery task to send welcome email."""
    from api.v1.app import app, mail
    # app = create_app()  # Create an instance of our Flask app
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
        
@celery_app.task
def send_activation_mail_task(msg_details: dict) -> str:
    """Celery task to send activation email."""
    from api.v1.app import app, mail
    with app.app_context():
        try:
            email = msg_details['email']
            company_id = msg_details['company_id']
            account = db.find_account_by(email=email, company_id=company_id)
            activation_session = SessionAuth()
            account.sessions.append(activation_session)
            db.save()
            account.tmp_token = activation_session.id
            account.save()
            activation_token = activation_session.id
            data = {
                "name": msg_details['name'],
                "company_id": company_id,
                "activation_link": "http://localhost:5000/api/v1/activate?"+
                "email={}&company_id={}&activation_token={}".format(
                    email, company_id, activation_token)
            }
            msg = Message(
                "Activate your HRPro account",
                sender=getenv('HRPRO_EMAIL'),
                recipients=[email]
            )
            msg.html = render_template("email_activation.html", data=data)
            mail.send(msg)
            return "task done successfully"
        except Exception as err:
            return "task failed" + str(err)

@celery_app.task
def send_reset_password_mail_task(msg_details: dict) -> str:
    """Celery task to send activation email."""
    from api.v1.app import app, mail
    with app.app_context():
        try:
            email = msg_details["email"]
            data = {
                "name": msg_details["name"],
                "company_id": msg_details["company_id"],
                "email": email,
                "password": msg_details["password"],
            }
            msg = Message(
                "Reset your HRPro password",
                sender=getenv('HRPRO_EMAIL'),
                recipients=[email]
            )
            msg.html = render_template("reset_password.html", data=data)
            mail.send(msg)
            return "task done successfully"
        except Exception as err:
            return "task failed" + str(err)
