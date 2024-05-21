from functools import wraps
from flask import request, abort
from api.v1.auth.auth import Auth


def requires_auth(allowed_roles=None):
    """Decorator to check for valid session and optional role requirement.

    Args:
        role: Optional string representing the required role for access.

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
                abort(401, description="Unauthorized: Missing session ID")

            account = Auth().get_account_from_session_id(session_id)
            if not account:
                abort(401, description="Unauthorized: Invalid session ID")

            if allowed_roles and account.role in allowed_roles:
                abort(403, description="Forbidden: Insufficient permissions")

            return func(*args, **kwargs)

        return decorated

    return wrapper
