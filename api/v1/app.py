#!/usr/bin/env python3

from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(exception):
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """ handle exception """
    return jsonify({"error": "Not found"}), 404


@app.route('/')
def hello():
    """ hello """
    return jsonify({"Hello": "HRPRO"})

if __name__ == "__main__":
    host = getenv("HRPRO_API_HOST", "0.0.0.0")
    port = getenv("HRPRO_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True, debug=True)
