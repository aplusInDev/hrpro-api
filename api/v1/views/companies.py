#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Company, Form, Field


@app_views.route('/companies', methods=['GET'], strict_slashes=False)
def get_companies():
    """ get companies """
    companies = storage.all(Company)
    all_companies = []
    for company in companies.values():
        company_dict = company.to_dict().copy()
        company_dict["employees"] = "http://localhost:5000/api/v1/companies/{}/employees".format(company.id)
        company_dict["jobs"] = "http://localhost:5000/api/v1/companies/{}/jobs".format(company.id)
        company_dict["departments"] = "http://localhost:5000/api/v1/companies/{}/departments".format(company.id)
        forms = {form.name: "http://localhost:5000/api/v1/forms/{}".format(form.id) for form in company.forms}
        company_dict["forms"] = forms
        company_dict["uri"] = "http://localhost:5000/api/v1/companies/{}".format(company.id)
        all_companies.append(company_dict)
    return jsonify(all_companies)

@app_views.route('/companies/<company_id>', methods=['GET'], strict_slashes=False)
def get_company(company_id):
    """ get company """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    company_dict = company.to_dict().copy()
    company_dict["employees"] = "http://localhost:5000/api/v1/companies/{}/employees".format(company_id)
    company_dict["jobs"] = "http://localhost:5000/api/v1/companies/{}/jobs".format(company_id)
    company_dict["departments"] = "http://localhost:5000/api/v1/companies/{}/departments".format(company_id)
    forms = [{
        "id": form.id ,"name": form.name,
        "uri": "http://localhost:5000/api/v1/forms/{}".format(form.id)} for form in company.forms]
    company_dict["forms"] = forms
    company_dict["uri"] = "http://localhost:5000/api/v1/companies/{}".format(company_id)
    return jsonify(company_dict)

@app_views.route('/companies', methods=['POST'], strict_slashes=False)
def post_company():
    """ post company """
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'name' not in data:
        return 'Missing name', 400
    company = Company(**data)
    company_dict = company.to_dict().copy()
    emp_form = Form(name="employee_form", company_id=company.id)
    dep_form = Form(name="department_form", company_id=company.id)
    job_form = Form(name="job_form", company_id=company.id)
    emp_form.fields.append(Field(fname="name", ftype="text", is_required=False, fposition=1))
    emp_form.fields.append(Field(fname="email", ftype="email", is_required=True, fposition=2))
    emp_form.fields.append(Field(fname="password", ftype="password", is_required=True, fposition=3))
    dep_form.fields.append(Field(fname="name", ftype="text", is_required=True, fposition=1))
    job_form.fields.append(Field(fname="name", ftype="text", is_required=True, fposition=1))
    for form in [emp_form, dep_form, job_form]:
        company.forms.append(form)
    company.save()
    company_dict["employees"] = "http://localhost:5000/api/v1/companies/{}/employees".format(company.id)
    company_dict["jobs"] = "http://localhost:5000/api/v1/companies/{}/jobs".format(company.id)
    company_dict["departments"] = "http://localhost:5000/api/v1/companies/{}/departments".format(company.id)
    company_dict["forms"] = "http://localhost:5000/api/v1/companies/{}/forms".format(company.id)
    company_dict["uri"] = "http://localhost:5000/api/v1/companies/{}".format(company.id)
    return jsonify(company_dict), 201

@app_views.route('/companies/<company_id>', methods=['PUT'], strict_slashes=False)
def put_company(company_id):
    """ put company """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'forms',
                       'employees', 'jobs', 'departments'
                       ]:
            setattr(company, key, value)
    company.save()
    company_dict = company.to_dict().copy()
    company_dict["employees"] = "http://localhost:5000/api/v1/companies/{}/employees".format(company_id)
    company_dict["jobs"] = "http://localhost:5000/api/v1/companies/{}/jobs".format(company_id)
    company_dict["departments"] = "http://localhost:5000/api/v1/companies/{}/departments".format(company_id)
    forms = [{
        "id": form.id ,"name": form.name,
        "url": "http://localhost:5000/api/v1/forms/{}".format(form.id)} for form in company.forms]
    company_dict["forms"] = forms
    company_dict["uri"] = "http://localhost:5000/api/v1/companies/{}".format(company_id)
    return jsonify(company_dict)

@app_views.route('/companies/<company_id>', methods=['DELETE'], strict_slashes=False)
def delete_company(company_id):
    """ delete company """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    company.delete()
    return jsonify({}), 200
