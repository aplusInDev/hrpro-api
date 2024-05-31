#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Company, Form, Field
from api.v1.auth.middleware import requires_auth


@app_views.route('/companies', methods=['GET'], strict_slashes=False)
def get_companies():
    """ get companies """
    companies = storage.all("Company")
    return jsonify([company.to_dict() for company in companies.values()])

@app_views.route('/companies/<company_id>', methods=['GET'], strict_slashes=False)
@requires_auth()
def get_company(company_id):
    """ get company """
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    return jsonify(company.to_dict())

@app_views.route('/companies', methods=['POST'], strict_slashes=False)
@requires_auth(["admin"])
def post_company():
    """ post company """
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'name' not in data:
        return 'Missing name', 400
    company = Company(**data)
    emp_form = Form(name="employee_form", company_id=company.id)
    dep_form = Form(name="department_form", company_id=company.id)
    job_form = Form(name="job_form", company_id=company.id)
    emp_form.fields.append(Field(name="name", type="text", is_required=False, position=1))
    emp_form.fields.append(Field(name="email", type="email", is_required=True, position=2))
    emp_form.fields.append(Field(name="password", type="password", is_required=True, position=3))
    dep_form.fields.append(Field(name="name", type="text", is_required=True, position=1))
    job_form.fields.append(Field(name="title", type="text", is_required=True, position=1))
    for form in [emp_form, dep_form, job_form]:
        company.forms.append(form)
    company.save()
    return jsonify(company.to_dict()), 201

@app_views.route('/companies/<company_id>', methods=['PUT'], strict_slashes=False)
@requires_auth(["admin"])
def put_company(company_id):
    """ put company """
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    data = request.form.to_dict()
    if data is None:
        return 'Not a JSON', 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'forms',
                       'employees', 'jobs', 'departments'
                       ]:
            setattr(company, key, value)
    company.save()
    return jsonify(company.to_dict())

@app_views.route('/companies/<company_id>', methods=['DELETE'], strict_slashes=False)
@requires_auth(["admin"])
def delete_company(company_id):
    """ delete company """
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    company.delete()
    return jsonify({}), 200
