from functools import wraps
from flask import request, abort, jsonify
from api.v1.auth.auth import Auth


def requires_auth(allowed_roles=None):
    """Decorator to check for valid session and optional role requirement.

    Args:
        role: Optional list of strings representing the required roles for access.

    Usage examples:
    # Usage examples (assuming these are view functions)
    @requires_auth()
    def some_view():
        # Accessible by any authenticated user
        pass

    @requires_auth(allowed_roles=["admin"])
    def admin_view():
        # Accessible only by admins
        pass

    @requires_auth(allowed_roles=["hr", "admin"])  # Assuming 'not_employee' means other roles
    def not_employee_view():
        # Accessible by anyone except employees
        pass


    Returns:
        The decorated function.
    """

    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            session_id = request.cookies.get('session_id')
            if not session_id:
                return jsonify({"error": "Unauthorized: Missing session ID"}), 401

            account = Auth().get_account_from_session_id(session_id)
            if not account:
                return jsonify({"error": "Unauthorized: Invalid session ID"}), 401
            
            if allowed_roles and account.role not in allowed_roles:
                return jsonify({"error": "Forbidden: Insufficient permissions"}), 403
            else:
                print("passed")

            return func(*args, **kwargs)

        return decorated

    return wrapper
