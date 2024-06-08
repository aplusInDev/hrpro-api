from flask_mail import Message
from os import getenv
from api.celery_app import app


@app.task
def send_welcome_mail_task(name, email, password):
    """Celery task to send welcome email."""
    from api.v1.app import create_app, mail
    app = create_app()  # Create an instance of your Flask app
    with app.app_context():  # Push the application context
        try:
            msg = Message("Welcome to HRPro", sender=getenv('HRPRO_EMAIL'),
                        recipients=[email])
            msg.html = f"""
                <div>
                    <h1>Welcome {name} to HRPro</h1>
                    <p>Your account has been created successfully.</p>
                    <p>Your password is: {password}</p>
                    <p>Click <a href="http://localhost:3000/login">here</a> to login.</p>
                </div>
            """
            mail.send(msg)
            return "task done successfully"
        except Exception as err:
            return "task failed" + str(err)
