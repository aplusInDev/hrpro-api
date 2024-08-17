#!/usr/bin/env python3
""" employees views """
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
def post_employee(employee_details):
    """ POST /add_employee
    """
    auth = Auth()
    employee_details["password"] = _generate_random_pass()
    try:
        account = auth.register_employee(employee_details)
        if account:
            msg_details = {
                "name": account.employee.first_name +
                    " " + account.employee.last_name,
                "company_id": account.company_id,
                "email": account.email,
                "password": employee_details["password"],
                "login_link": "http://localhost:3000/login",
            }
            send_welcome_mail_task.delay(msg_details)
            return jsonify(account.employee.to_dict()), 202
    except ValueError as err:
        return jsonify({"error": 'ValueError: {}'.format(str(err))}), 400
    except Exception as err:
        return jsonify({"error": "Exception: {}".format(str(err))}), 500

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
        return {"error": "Not a json"}, 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            if key == 'department' or key == 'department_name':
                department = storage.find_department_by(
                    company_id=employee.company_id,
                    name=value,
                )
                if department is None:
                    continue
                employee.department = department
            elif key == 'job' or key == 'job_title':
                job = storage.find_job_by(
                    company_id=employee.company_id,
                    title=value,
                )
                if job is None:
                    continue
                else:
                    employee.job = job
            else:
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
        return {"error": "Not a valid data"}, 400
    else:
        from api.v1.utils.form_utils import handle_update_info
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                if hasattr(employee, key):
                    setattr(employee, key, value)
        try:
            data = handle_update_info("employee", employee.company_id, data)
            employee.info = str(data)
            employee.save()
            return jsonify(eval(employee.info)), 200
        except ValueError as err:
            return jsonify({"error": "- ValueError - {}".format(str(err))}), 400

@app_views.route(
        '/employees/<employee_id>', methods=['DELETE'], strict_slashes=False)
def delete_employee(employee_id):
    """ delete employee """
    auth = Auth()
    employee = storage.get("Employee", employee_id)
    if employee is None:
        abort(404)
    employee.delete()
    account = auth._db.find_account_by(employee_id=employee_id)
    if account:
        auth._db.delete_account(account.id)
    return jsonify({}), 204
