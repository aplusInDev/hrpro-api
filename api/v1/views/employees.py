#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Company, Employee


@app_views.route('/companies/<company_id>/employees', methods=['GET'], strict_slashes=False)
def get_employees(company_id):
    """ get employees """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    all_employees = []
    for employee in company.employees:
        employee_dict = employee.to_dict().copy()
        employee_dict["uri"] = "http://localhost:5000/api/v1/employees/{}".format(employee.id)
        del employee_dict["info"]
        all_employees.append(employee_dict)
    return jsonify(all_employees)

@app_views.route('/employees/<employee_id>', methods=['GET'], strict_slashes=False)
def get_employee(employee_id):
    """ get employee """
    employee = storage.get(Employee, employee_id)
    if employee is None:
        abort(404)
    employee_dict = employee.to_dict().copy()
    employee_dict["uri"] = "http://localhost:5000/api/v1/employees/{}".format(employee.id)
    employee_dict["info"] = eval(employee.info)
    return jsonify(employee_dict)

@app_views.route('/companies/<company_id>/employees', methods=['POST'], strict_slashes=False)
def post_employee(company_id):
    """ post employee """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'info' not in data:
        return 'Employee informations missing', 400
    employee = Employee(**data)
    employee.company_id = company_id
    employee.save()
    return jsonify(employee.to_dict()), 201

@app_views.route('/employees/<employee_id>', methods=['PUT'], strict_slashes=False)
def put_employee(employee_id):
    """ put employee """
    employee = storage.get(Employee, employee_id)
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

@app_views.route('/employees/<employee_id>/info', methods=['PUT'], strict_slashes=False)
def put_employee_info(employee_id):
    """ put employee info """
    employee = storage.get(Employee, employee_id)
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
        return jsonify(employee.to_dict())

@app_views.route('/employees/<employee_id>', methods=['DELETE'], strict_slashes=False)
def delete_employee(employee_id):
    """ delete employee """
    employee = storage.get(Employee, employee_id)
    if employee is None:
        abort(404)
    employee.delete()
    return jsonify({}), 204
