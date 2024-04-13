#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Department, Company


@app_views.route('companies/<company_id>/departments', methods=['GET'], strict_slashes=False)
def get_departments(company_id):
    """ get departments """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    all_departments = [department.to_dict() for department in company.departments]
    return jsonify(all_departments)

@app_views.route('departments/<department_id>', methods=['GET'], strict_slashes=False)
def get_department(department_id):
    """ get department """
    department = storage.get(Department, department_id)
    if department is None:
        abort(404)
    return jsonify(department.to_dict())

@app_views.route('companies/<company_id>/departments', methods=['POST'], strict_slashes=False)
def post_department(company_id):
    """ post department """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    department = Department(**data)
    department.company_id = company_id
    department.save()
    return jsonify(department.to_dict()), 201

@app_views.route('departments/<department_id>', methods=['PUT'], strict_slashes=False)
def put_department(department_id):
    """ put department """
    department = storage.get(Department, department_id)
    if department is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(department, key, value)
    department.save()
    return jsonify(department.to_dict())

@app_views.route('departments/<department_id>', methods=['DELETE'], strict_slashes=False)
def delete_department(department_id):
    """ delete department """
    department = storage.get(Department, department_id)
    if department is None:
        abort(404)
    department.delete()
    return jsonify({}), 200
