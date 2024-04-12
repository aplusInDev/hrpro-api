#!/usr/bin/env python3

from flask import jsonify
from api.v1.views import app_views
from models import *


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ status """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ stats """
    return jsonify({"stats": 200})
