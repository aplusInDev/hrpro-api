#!/usr/bin/env python3

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views
from flask_mail import Mail, Message


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}}, supports_credentials=True)
app.register_blueprint(app_views, )


app.config.update(
    MAIL_SERVER='smtp.aplusdev.tech',
    MAIL_PORT=25,  # 25 or 587
    MAIL_USE_SSL=False,
    MAIL_USERNAME=getenv('HRPRO_EMAIL'),
    MAIL_PASSWORD=getenv('HRPRO_EMAIL_PWD')
)
mail = Mail(app)

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.update(
        MAIL_SERVER='smtp.aplusdev.tech',
        MAIL_PORT=25,  # 25 or 587
        MAIL_USE_SSL=False,
        MAIL_USERNAME=getenv('HRPRO_EMAIL'),
        MAIL_PASSWORD=getenv('HRPRO_EMAIL_PWD')
    )
    mail.init_app(app)

    with app.app_context():
        # Include our Views
        from api.v1.views import app_views

        # Register Blueprints
        app.register_blueprint(app_views)

        return app


@app.route('/send_mail', methods=['POST'])
def send_mail():
    """ POST /test_mail
    """
    msg = Message("hello test", sender=getenv('HRPRO_EMAIL'),
                  recipients=[
                      "laabid.abdessamadplus@gmail.com",
                      "aeots2018@gmail.com"
                ])
    data = {
        "recipient_name": "Aplus",
        "activation_link": "localhost/api/v1/companies"
    }
    html_content = """
        <div class="info">
        {{ data.activation_link|safe }}
        </div>
    """
    msg.html = render_template(html_content, data=data)
    try:
        mail.send(msg)
        return jsonify({"message": "mail sent"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 400

@app.teardown_appcontext
def close_storage(exception):
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """ handle exception """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(e):
    """ handle exception """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(e):
    """ handle exception """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("HRPRO_API_HOST", "0.0.0.0")
    port = getenv("HRPRO_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True, debug=True)
