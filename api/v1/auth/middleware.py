from functools import wraps
from flask import request, jsonify
from os import getenv
from api.v1.auth.auth import Auth
from sqlalchemy.orm.exc import NoResultFound


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
            env = getenv('HRPRO_ENV')
            if env == 'test':
                return func(*args, **kwargs)
            session_id = request.cookies.get('session_id')
            if not session_id:
                return jsonify({
                    "error": "Unauthorized: Missing session ID"
                }), 401
            try:
                account = Auth().get_account_from_session_id(session_id)
            except NoResultFound as err:
                return jsonify({
                    "error": "Unauthorized: Invalid session ID"
                }), 401
            except Exception as err:
                return jsonify({
                    "error": str(err)
                })
            
            if allowed_roles and account.role not in allowed_roles:
                return jsonify({
                    "error": "Forbidden: Insufficient permissions"
                }), 403

            return func(*args, **kwargs)

        return decorated

    return wrapper
