#!/usr/bin/env python3

from flask import jsonify, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth, _hash_password, _generate_random_pass
from api.v1.utils.accounts_utils import validate_register
from api.v1.helpers.tasks.mail_tasks import (
    send_activation_mail_task,
    send_reset_password_mail_task,
)
from sqlalchemy.orm.exc import NoResultFound
from api.v1.auth import db


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
            "message": "Account created successfully. Please check your"+
            "email for your login information"
            }), 202
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 400

@app_views.route('/reset_password', methods=['POST'])
def reset_password():
    """ POST /reset_password
    """
    for field in ["email", "company_id"]:
        if field not in request.form:
            return jsonify({
                "error": "filed {} is required".format(field)
            }), 401
    email = request.form.get('email')
    company_id = request.form.get('company_id')
    try:
        account = db.find_account_by(email=email, company_id=company_id)
    except NoResultFound as err:
        return jsonify({"error": str(err)}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 400
    password = _generate_random_pass()
    hashed_password = _hash_password(password)
    account.hashed_password = hashed_password
    account.save()
    name = account.employee.first_name + " " + account.employee.last_name
    msg_details = {
        "name": name,
        "email": email,
        "company_id": company_id,
        "password": password
    }
    send_reset_password_mail_task.delay(msg_details)
    return jsonify({"message": "your next login informations has been sent to your email"}), 202

@app_views.route("/update_password", methods=["POST"])
def update_password():
    """ POST /update_password """
    for field in ["password", "new_password"]:
        if field not in request.form:
            return jsonify({
                "error": "filed {} is required".format(field)
            }), 400
    password = request.form.get('password')
    new_password = request.form.get('new_password')
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({"error": "Unauthorized: Missing session ID"}), 401
    login_details = {
        "session_id": session_id,
        "password": password,
        "new_password": new_password,
    }
    try:
        auth = Auth()
        auth.update_password(login_details)
        return jsonify({"message": "Password updated successfully"}), 200
    except ValueError as err:
        return jsonify({"error": "ValueError: {}".format(str(err))}), 403
    except NoResultFound:
        return jsonify({"error": "Account Not Found"}), 403
    except Exception as err:
        return jsonify({"error": "Exception: {}".format(str(err))}), 403
