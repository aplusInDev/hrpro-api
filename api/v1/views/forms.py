#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Form, Company
from api.v1.utils import is_exists_form


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
        form_dict["uri"] = "http://localhost:5000/api/v1/forms/{}".format(form.id)
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
    form_fields = []
    for field in form.fields:
        field_dict = field.to_dict().copy()
        field_dict["uri"] = "http://localhost:5000/api/v1/fields/{}".format(field.id)
        form_fields.append(field_dict)
    form_dict["fields"] = form_fields
    form_dict["uri"] = "http://localhost:5000/api/v1/forms/{}".format(form_id)
    return jsonify(form_dict)

@app_views.route('/companies/<company_id>/forms', methods=['POST'], strict_slashes=False)
def post_form(company_id):
    """ post form """
    data = request.get_json()
    if data is None:
        return 'Not a JSON data', 400
    elif 'name' not in data:
        return 'Missing name', 400
    else:
        if is_exists_form(company_id, data):
            return jsonify({"error": "form name already exists"}), 400
        form = Form(company_id=company_id, **data)
        form.save()
        form_dict = form.to_dict().copy()
        form_dict["company"] = "http://localhost:5000/api/v1/companies/{}".format(company_id)
        form_dict["uri"] = "http://localhost:5000/api/v1/forms/{}".format(form.id)
        return jsonify(form_dict), 201

@app_views.route('/forms/<form_id>', methods=['PUT'], strict_slashes=False)
def put_form(form_id):
    """ put form """
    form = storage.get(Form, form_id)
    if form is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON data', 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at',
                        'company', 'fields']:
                setattr(form, key, value)
    form.save()
    form_dict = form.to_dict().copy()
    form_dict["company"] = "http://localhost:5000/api/v1/companies/{}".format(form.company.id)
    form_dict["fields"] = [field.to_dict() for field in form.fields]
    form_dict["uri"] = "http://localhost:5000/api/v1/forms/{}".format(form_id)
    return jsonify(form_dict)

@app_views.route('/forms/<form_id>', methods=['DELETE'], strict_slashes=False)
def delete_form(form_id):
    """ delete form """
    form = storage.get(Form, form_id)
    if form is None:
        abort(404)
    form.delete()
    return jsonify({}), 200
