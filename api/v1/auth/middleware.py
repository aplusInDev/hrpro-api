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

def validate_register(func):
    """ Decorator to validate the register account request.
    Args:
        func: The view function to be decorated.
    Returns:
        The decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        if not first_name:
            return jsonify({"error": "first name is required"}), 400
        if not last_name:
            return jsonify({"error": "last name is required"}), 400
        if not email:
            return jsonify({"error": "email is required"}), 400
        if not password:
            return jsonify({"error": "password is required"}), 400
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        return func(data, *args, **kwargs)
    return wrapper
