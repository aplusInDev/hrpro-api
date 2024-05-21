#!/usr/bin/env python3

from functools import wraps
from flask import request, redirect, jsonify
from api.v1.auth.auth import Auth


def session_required(func):
    """Decorator to check for a valid session ID in the request cookies.

    Args:
        func: The view function to be decorated.

    Returns:
        The decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id:
            return jsonify({"error": "forbidden"}), 403

        account = Auth().get_account_from_session_id(session_id)

        if not account:
            return jsonify({"error": "forbidden"}), 403

        return func(account, *args, **kwargs)

    return wrapper

# def validate_register(func):
#     """ Decorator to validate the register account request.
#     Args:
#         func: The view function to be decorated.
#     Returns:
#         The decorated function.
#     """
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         required_fields = [
#             'first_name', 'last_name', 'email', 'password',
#             'company_name', 'company_address'
#             ]
#         for field in required_fields:
#             if field not in request.form:
#                 msg = f"{field} is required"
#                 return jsonify({"error": msg}), 400
#         company_info = {}
#         admin_info = {}
#         for key, value in request.form.items():
#             if "company_" in key:
#                 company_info[key.split("company_")[1]] = value
#             else:
#                 admin_info[key] = value
#         return func(admin_info, company_info, *args, **kwargs)
#     return wrapper
