#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Department, Company
from api.v1.auth.middleware import session_required


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
@session_required
def post_department(account, company_id):
    """ post department """
    if account.role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    data = request.form
    if not data:
        return jsonify({"error": "unvalid request"}), 400

    from api.v1.utils.validate_field import handle_update_info
    data = data.to_dict()
    data = handle_update_info("department", company_id, data)
    if data:
        data = str(data)
        new_department = Department(info=data, company_id=company_id)
        new_department.save()
        return jsonify(new_department.to_dict())

    return jsonify({"error": "unvalid request"}), 400
    

@app_views.route('departments/<department_id>', methods=['PUT'], strict_slashes=False)
@session_required
def put_department(account, department_id):
    """ put department """
    if account.role != "admin":
        abort(401)
    department = storage.get(Department, department_id)
    if department is None:
        abort(404)
    data = request.form
    if not data:
        return jsonify({"error": "unvalid request"}), 400
    from api.v1.utils.validate_field import handle_update_info
    data = data.to_dict()
    data = handle_update_info("department", department.company_id, data)
    if data:
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
