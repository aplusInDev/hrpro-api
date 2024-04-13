#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Company


@app_views.route('/companies', methods=['GET'], strict_slashes=False)
def get_companies():
    """ get companies """
    companies = storage.all(Company)
    all_companies = []
    for company in companies.values():
        company_dict = company.to_dict().copy()
        company_dict = company.to_dict().copy()
        company_dict["employees"] = "http://localhost:5000/api/v1/companies/{}/employees".format(company.id)
        company_dict["jobs"] = "http://localhost:5000/api/v1/companies/{}/jobs".format(company.id)
        company_dict["departments"] = "http://localhost:5000/api/v1/companies/{}/departments".format(company.id)
        forms = {form.name: "http://localhost:5000/api/v1/forms/{}".format(form.id) for form in company.forms}
        company_dict["forms"] = forms
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
    forms = {form.name: "http://localhost:5000/api/v1/forms/{}".format(form.id) for form in company.forms}
    company_dict["forms"] = forms
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
    company.save()
    return jsonify(company.to_dict()), 201

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
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(company, key, value)
    company.save()
    return jsonify(company.to_dict())

@app_views.route('/companies/<company_id>', methods=['DELETE'], strict_slashes=False)
def delete_company(company_id):
    """ delete company """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    company.delete()
    return jsonify({}), 200
