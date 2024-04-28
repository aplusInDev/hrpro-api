#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

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
