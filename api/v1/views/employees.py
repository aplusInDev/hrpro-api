#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from api.v1.utils.accounts_utils import validate_post_employee
from api.v1.auth.auth import Auth, _generate_random_pass
from api.v1.helpers.tasks.mail_tasks import send_welcome_mail_task


@app_views.route(
        '/companies/<company_id>/employees', methods=['GET'],
        strict_slashes=False)
def get_employees(company_id):
    """ get employees """
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    return jsonify([employee.to_dict() for employee in company.employees])

@app_views.route(
        '/companies/<company_id>/employees_names', methods=['GET'],
        strict_slashes=False)
def get_employees_names(company_id):
    """ get employees names """
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    employees_names = []
    for employee in company.employees:
        employees_names.append(employee.first_name + " " + employee.last_name)
    return jsonify(employees_names)

@app_views.route(
        '/employees/<employee_id>', methods=['GET'],
        strict_slashes=False)
def get_employee(employee_id):
    """ get employee """
    employee = storage.get("Employee", employee_id)
    if employee is None:
        abort(404)
    return jsonify(employee.to_dict())

@app_views.route('/add_employee', methods=['POST'])
@validate_post_employee
def post_employee(account_info, position_info):
    """ POST /add_employee
    """
    auth = Auth()
    account_info["password"] = _generate_random_pass()
    try:
        account = auth.add_employee_account(account_info, position_info)
        if account:
            send_welcome_mail_task.delay(account.first_name,
                                   account.email, account_info["password"])
    except ValueError as err:
        return jsonify({"valueError": str(err)}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    return jsonify({"email": account.email, "message": "employee added"}), 202

@app_views.route(
        '/employees/<employee_id>', methods=['PUT'],
        strict_slashes=False)
def put_employee(employee_id):
    """ put employee """
    employee = storage.get("Employee", employee_id)
    if employee is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(employee, key, value)
    employee.save()
    return jsonify(employee.to_dict())

@app_views.route(
        '/employees/<employee_id>/info', methods=['PUT'],
        strict_slashes=False)
def put_employee_info(employee_id):
    """ put employee info """
    employee = storage.get("Employee", employee_id)
    if employee is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not valid data', 400
    else:
        from api.v1.utils.validate_field import handle_update_info
        data = handle_update_info("employee", employee.company_id, data)
        employee.info = str(data)
        employee.save()
        return jsonify(eval(employee.info))

@app_views.route(
        '/employees/<employee_id>', methods=['DELETE'], strict_slashes=False)
def delete_employee(employee_id):
    """ delete employee """
    employee = storage.get("Employee", employee_id)
    if employee is None:
        abort(404)
    employee.delete()
    return jsonify({}), 204
