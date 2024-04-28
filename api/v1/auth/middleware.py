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
