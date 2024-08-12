#!/usr/bin/env python3

from flask import jsonify, request, make_response
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from sqlalchemy.orm.exc import NoResultFound
from api.v1.auth import db


@app_views.route('/activate', methods=['GET'])
def activate_account():
    """ GET /activate
    """
    auth = Auth()
    try:
        company_id = request.args.get('company_id')
        activation_token = request.args.get('activation_token')
        email = request.args.get("email")
        for field in [company_id, activation_token, email]:
            if not field:
                return jsonify({"error": "missing required fields"}), 400
        account = db.find_account_by(
            email=email,
            company_id=company_id
        )
        auth.activate_account(account.id, activation_token)
        return "<h1>Account activated</h1>", 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 403
    except NoResultFound:
        return jsonify(
            {"error": "Faild to activate account, please try again"}
        )

@app_views.route('/login', methods=['POST'])
def login():
    """ POST /session
    """
    from api.v1.auth import db
    for field in ["email", "password", "company_id"]:
        if field not in request.form:
            return jsonify({
                "error": "filed {} is required".format(field)
            }), 401
    email = request.form.get('email')
    password = request.form.get('password')
    company_id = request.form.get('company_id')
    auth = Auth()
    if auth.valid_login(company_id, email, password):
        account = db.find_account_by(email=email, company_id=company_id)
        if not account.is_active and account.role == 'admin':
            return jsonify({
                "error": "Your account is not activated yet,"+
                " please check your email to activate it."
            }), 401
        session_id = auth.create_session(company_id, email)
        if session_id:
            current_user = auth.get_current_user(company_id, email)
            response = jsonify(current_user)
            response.set_cookie('session_id', session_id)
            response = make_response(jsonify(response))
            response.headers['Access-Control-Expose-Headers'] = 'Set-Cookie'
            return response, 200
            # return response, 200
    return jsonify({"error": "Login Faild, please try again."}), 401

@app_views.route('/profile', methods=['GET'])
def get_profile():
    """ GET /profile
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({"error": "session not found"}), 403
    auth = Auth()
    try:
        account = auth.get_account_from_session_id(session_id)
        return jsonify(account.employee.to_dict()), 200
    except NoResultFound:
        return jsonify({"error": "session not found"}), 403

@app_views.route('/check_login', methods=['GET'])
def check_login():
    """ GET /check_login """
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({"message": "session not found"}), 200
    try:
        auth = Auth()
        auth.get_account_from_session_id(session_id)
        return jsonify({"message": "ok"}), 200
    except NoResultFound:
        return jsonify({"message": "session not found"}), 200

@app_views.route('/logout', methods=['DELETE'])
def logout():
    """ DELETE /sessions
    The request is expected to contain the session ID as a cookie with
    key = session_id
    If the account exists it destroy the session and redirect the account to GET /
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({"error": "session not found"}), 403
    auth = Auth()
    if auth.destroy_session(session_id):
        return jsonify({"message": "logged out successfully"}), 200
    return jsonify({"error": "session not found"}), 403
