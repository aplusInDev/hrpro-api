#!/usr/bin/env python3

from flask import jsonify, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth, _hash_password, _generate_random_pass
from api.v1.auth.middleware import session_required, validate_register
from models import storage


@app_views.route('/accounts', methods=['POST'])
@validate_register
def register_account(admin_info: dict, company_info: dict):
    """ POST /accounts
    """
    auth = Auth()
    try:
        account = auth.register_account(admin_info, company_info, role="admin")
        # auth.send_activation_mail(account.email, account.first_name)
        return jsonify({
            "email": account.email,
            "message": "account created"
            }), 201
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

@app_views.route('/add_employee', methods=['POST'])
@session_required
def add_employee(account):
    """ POST /add_employee
    """
    if account.role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    required_fields = ['first_name', 'last_name', 'email']
    if 'role' not in request.form or 'role' == 'emplyee':
        required_fields = [*required_fields, "department", "job title"]
    for field in required_fields:
        if field not in request.form:
            return jsonify({"error": "missing information"}), 400
        employee_info = request.form.to_dict().copy()
    auth = Auth()
    try:
        password = _generate_random_pass()
        hashed_password = _hash_password(password)
        employee_info["role"] = request.form.get("role", "employee")
        employee_info["is_active"] = True
        employee_info["hashed_password"] = hashed_password
        company_info = {
            "employee_id": account.employee_id,
        }
        employee = auth._db.add_account(employee_info, company_info)
        auth.send_welcome_mail(employee.first_name, employee.email, password)
        return jsonify({
            "email": employee.email,
            "message": "employee added"
            }), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 400

@app_views.route('/profile', methods=['GET'])
@session_required
def profile(account):
    """ GET /profile
    The request is expected to contain the session ID as a cookie with
    key = session_id
    If the account exists it returns the account email
    """
    employee_info = storage.get_emplyee_info(account.employee_id)
    return jsonify(employee_info), 200

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
