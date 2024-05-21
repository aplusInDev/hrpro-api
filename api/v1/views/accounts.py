#!/usr/bin/env python3

from flask import jsonify, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth, _generate_random_pass
from api.v1.utils.accounts_utils import (
    validate_register,
    validate_post_employee
    )


@app_views.route('/accounts', methods=['POST'])
@validate_register
def post_admin(admin_info: dict, company_info: dict):
    """ POST /accounts
    """
    auth = Auth()
    try:
        account = auth.register_admin(admin_info, company_info)
        # auth.send_activation_mail(account.email, account.first_name)
        return jsonify({
            "email": account.email,
            "message": "account created"
            }), 201
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

@app_views.route('/add_employee', methods=['POST'])
@validate_post_employee
def post_employee(account_info, position_info):
    """ POST /add_employee
    """
    auth = Auth()
    account_info["hashed_password"] = _generate_random_pass()
    try:
        account = auth.add_employee_account(account_info, position_info)
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    return jsonify({"email": account.email, "message": "employee added"}), 201

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
