#!/usr/bin/env python3
""" Forms views """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Form


@app_views.route('/companies/<company_id>/forms', methods=['GET'], strict_slashes=False)
def get_forms(company_id):
    """ get forms """
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    return jsonify([form.to_dict() for form in company.forms])

@app_views.route('/forms/<form_id>', methods=['GET'], strict_slashes=False)
def get_form(form_id):
    """ get form """
    form = storage.get("Form", form_id)
    if form is None:
        abort(404)
    return jsonify(form.to_dict())

@app_views.route('/companies/<company_id>/forms', methods=['POST'], strict_slashes=False)
def post_form(company_id):
    """ post form """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON data'}), 400
    elif 'name' not in data:
        return {'error': 'Missing name'}, 400
    else:
        form_name = data['name']
        form = storage.find_form_by_(
                name=form_name,
                company_id=company_id,
            )
        if form:
            return jsonify({
                "error": "{} Form already exists".format(form_name)
            }), 400
        form = Form(company_id=company_id, **data)
        form.save()
        return jsonify(form.to_dict()), 201

@app_views.route('/forms/<form_id>', methods=['PUT'], strict_slashes=False)
def put_form(form_id):
    """ put form """
    form = storage.get("Form", form_id)
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
    return jsonify(form.to_dict())

@app_views.route('/forms/<form_id>', methods=['DELETE'], strict_slashes=False)
def delete_form(form_id):
    """ delete form """
    form = storage.get("Form", form_id)
    if form is None:
        abort(404)
    form.delete()
    return jsonify({}), 200
