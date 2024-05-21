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
    return jsonify([d.to_dict() for d in company.departments]), 200

@app_views.route('companies/<company_id>/departments_names', methods=['GET'])
def get_departments_names(company_id):
    """ get departments names """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    all_departments = []
    for department in company.departments:
        all_departments.append(department.name)
    return jsonify(all_departments), 200

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
    data = request.form
    if not data:
        return jsonify({"error": "Not a form data"}), 400

    from api.v1.utils.validate_field import handle_update_info
    data = data.to_dict()
    data = handle_update_info("department", company_id, data)
    if data and data.get("name", None):
        dep_name = data.get("name")
        data = str(data)
        new_department = Department(name=dep_name, info=data, company_id=company_id)
        new_department.save()
        return jsonify(new_department.to_dict())

    return jsonify({"error": "unvalid request"}), 400
    

@app_views.route('departments/<department_id>', methods=['PUT'], strict_slashes=False)
def put_department(department_id):
    """ put department """
    department = storage.get(Department, department_id)
    if department is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a json data"}), 400
    from api.v1.utils.validate_field import handle_update_info
    data = handle_update_info("department", department.company_id, data)
    if data:
        if 'name' in data:
            department.name = data.get('name')
        department.info = str(data)
        department.save()
        return jsonify(department.to_dict())
    return jsonify({"error": "unvalid request"}), 400

@app_views.route('departments/<department_id>', methods=['DELETE'], strict_slashes=False)
def delete_department(department_id):
    """ delete department """
    department = storage.get(Department, department_id)
    if department is None:
        abort(404)
    department.delete()
    return jsonify({}), 200
