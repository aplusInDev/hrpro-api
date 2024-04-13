#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from api.v1.utils import is_exists_form
from models import storage, Form, Company, Field
import json


@app_views.route('/companies/<company_id>/forms', methods=['GET'], strict_slashes=False)
def get_forms(company_id):
    """ get forms """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    all_forms = []
    for form in company.forms:
        form_dict = form.to_dict().copy()
        form_dict["company"] = "http://localhost:5000/api/v1/companies/{}".format(company_id)
        form_dict["fields"] = {field.fname: "http://localhost:5000/api/v1/fields/{}".format(field.id) for field in form.fields}
        all_forms.append(form_dict)
    return jsonify(all_forms)

@app_views.route('/forms/<form_id>', methods=['GET'], strict_slashes=False)
def get_form(form_id):
    """ get form """
    form = storage.get(Form, form_id)
    if form is None:
        abort(404)
    form_dict = form.to_dict().copy()
    form_dict["company"] = "http://localhost:5000/api/v1/companies/{}".format(form.company.id)
    form_dict["fields"] = [field.to_dict() for field in form.fields]
    return jsonify(form_dict)

@app_views.route('/companies/<company_id>/forms', methods=['POST'], strict_slashes=False)
def post_form(company_id):
    """ post form """
    data = request.get_json()
    if is_exists_form(company_id, data):
        return 'Not valid data', 400
    else:
        form = Form(name=data['name'], company_id=company_id)
        form_dict = form.to_dict().copy()
        for field in data['fields']:
            form.fields.append(Field(**field))
        form.save()
        return jsonify(form_dict), 201

@app_views.route('/forms/<form_id>', methods=['PUT'], strict_slashes=False)
def put_form(form_id):
    """ put form """
    form = storage.get(Form, form_id)
    if form is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(form, key, value)
    form.save()
    return jsonify(form.to_dict())

@app_views.route('/forms/<form_id>', methods=['DELETE'], strict_slashes=False)
def delete_form(form_id):
    """ delete form """
    form = storage.get(Form, form_id)
    if form is None:
        abort(404)
    form.delete()
    return jsonify({}), 200
