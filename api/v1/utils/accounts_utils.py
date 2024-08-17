#!/user/bin/env python3

from flask import jsonify, request
from functools import wraps
from api.v1.auth.auth import Auth


def validate_register(func):
    """ Decorator to validate the register account request.
    Args:
        func: The view function to be decorated.
    Returns:
        The decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        required_fields = [
            'first_name', 'last_name', 'email', 'password',
            'company_name', 'company_address'
            ]
        for field in required_fields:
            if field not in request.form:
                msg = f"{field} is required"
                return jsonify({"error": msg}), 400
        company_info = {}
        admin_info = {}
        for key, value in request.form.items():
            if "company_" in key:
                company_info[key.split("company_")[1]] = value
            else:
                admin_info[key] = value
        return func(admin_info, company_info, *args, **kwargs)
    return wrapper

def validate_post_employee(func):
    """ Decorator to validate the post employee request.
    Args:
        func: The view function to be decorated.
    Returns:
        The decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id:
            return jsonify({"error": "Unauthorized"}), 401
        account = Auth().get_account_from_session_id(session_id)
        if not account:
            return jsonify({"error": "Invalid login"}), 400
        required_fields = ['first_name', 'last_name', 'email']
        role = request.form.get('role', 'employee')
        if role != 'hr':
            required_fields = [*required_fields, "department", "job_title"]
        for field in required_fields:
            if field not in request.form:
                return jsonify({"error": "missing information"}), 400
        if role == 'hr':
            department = request.form.get("department", "hr")
            job_title = request.form.get("job_title", "hr")
        else:
            department = request.form.get("department")
            job_title = request.form.get("job_title")
        employee_details = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "role": role,
            "department": department,
            "job_title": job_title,
            "company_id": account.company_id,
        }
        return func(employee_details, *args, **kwargs)
    return wrapper
