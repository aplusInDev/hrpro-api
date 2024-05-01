#!/usr/bin/env python3

from flask import jsonify, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.middleware import session_required, validate_register


@app_views.route('/accounts', methods=['POST'])
@validate_register
def register_account(data):
    """ POST /accounts
    """
    auth = Auth()
    try:
        account = auth.register_account(**data, role="admin")
        # auth.send_activation_mail(account.email, account.first_name)
        return jsonify({
            "email": account.email,
            "message": "account created"
            }), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app_views.route('/profile', methods=['GET'])
@session_required
def profile(account):
    """ GET /profile
    The request is expected to contain the session ID as a cookie with
    key = session_id
    If the account exists it returns the account email
    """
    return jsonify({"email": account.email}), 200

@app_views.route('/reset_password', methods=['PUT'])
def update_password():
    """ PUT /reset_password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    password = request.form.get('password')
    if not reset_token:
        return jsonify({"error": "reset_token is required"}), 400
    if not password:
        return jsonify({"error": "password is required"}), 400
    auth = Auth()
    try:
        auth.update_password(reset_token, password)
        return jsonify({"email": email, "message": "password updated"}), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 403
