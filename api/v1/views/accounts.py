#!/usr/bin/env python3

from flask import jsonify, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.utils.accounts_utils import validate_register
from api.v1.helpers.tasks.mail_tasks import send_activation_mail_task


@app_views.route('/accounts', methods=['POST'])
@validate_register
def post_admin(admin_info: dict, company_info: dict):
    """ POST /accounts
    """
    auth = Auth()
    try:
        account = auth.register_admin(admin_info, company_info)
        msg_details = {
            "name": account.employee.first_name +
                " " + account.employee.last_name,
            "email": account.email,
            "company_id": account.company_id,
        }
        send_activation_mail_task.delay(msg_details)
        return jsonify({
            "email": account.email,
            "message": "account created"
            }), 202
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 400

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
    except Exception as err:
        return jsonify({"error": str(err)}), 403
