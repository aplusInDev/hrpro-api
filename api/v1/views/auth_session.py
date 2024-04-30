#!/usr/bin/env python3

from flask import jsonify, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.views import hello
from os import getenv


@app_views.route('/activate', methods=['GET'])
def activate_account():
    """ GET /activate
    """
    auth = Auth()
    try:
        account_id = request.args.get('account_id')
        activation_token = request.args.get('activation_token')
        auth.activate_account(account_id, activation_token)
        return jsonify({"message": "account activated"}), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 403

@app_views.route('/login', methods=['POST'])
def login():
    """ POST /session
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email is required"}), 400
    if not password:
        return jsonify({"error": "password is required"}), 400
    auth = Auth()
    try:
        if auth.valid_login(email, password):
            session_id = auth.create_session(email)
            if session_id:
                response = jsonify({"email": email, "message": "logged in"})
                response.set_cookie('session_id', session_id)
                return response, 200
        return jsonify({"error": "Uncorrect email or password"}), 401
    except ValueError:
        return jsonify({"message": "check your email and activate your account"}), 403


@app_views.route('/logout', methods=['DELETE'])
def logout():
    """ DELETE /sessions
    The request is expected to contain the session ID as a cookie with
    key = session_id
    If the account exists it destroy the session and redirect the account to GET /
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        auth = Auth()
        if auth.destroy_session(session_id):
            return hello(), 200
        return jsonify({"error": "session not found"}), 403

@app_views.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """ POST /reset_password
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email is required"}), 400
    auth = Auth()
    try:
        reset_token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        return jsonify({"error": "email not found"}), 403
