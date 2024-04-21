#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Form, Company, Field


@app_views.route('forms/<form_id>/fields', methods=['GET'], strict_slashes=False)
def get_fields(form_id):
	""" get fields """
	form = storage.get(Form, form_id)
	if form is None:
		abort(404)
	all_fields = []
	for field in form.fields:
		field_dict = field.to_dict().copy()
		field_dict["company"] = "http://localhost:5000/api/v1/companies/{}".format(form.company.id)
		field_dict["form"] = "http://localhost:5000/api/v1/forms/{}".format(form_id)
		field_dict["uri"] = "http://localhost:5000/api/v1/fields/{}".format(field.id)
		all_fields.append(field_dict)
	return jsonify(all_fields)

@app_views.route('/fields/<field_id>', methods=['GET'], strict_slashes=False)
def get_field(field_id):
	""" get field """
	field = storage.get(Field, field_id)
	if field is None:
		abort(404)
	field_dict = field.to_dict().copy()
	field_dict["company"] = "http://localhost:5000/api/v1/companies/{}".format(field.form.company.id)
	field_dict["form"] = "http://localhost:5000/api/v1/forms/{}".format(field.form.id)
	field_dict["uri"] = "http://localhost:5000/api/v1/fields/{}".format(field.id)
	return jsonify(field_dict)

@app_views.route('/forms/<form_id>/fields', methods=['POST'], strict_slashes=False)
def post_field(form_id):
	""" post field """
	form = storage.get(Form, form_id)
	if form is None:
		abort(404)
	data = request.get_json()
	if data is None:
		return 'Not a JSON data', 400
	elif 'fname' not in data:
		return 'Missing fname', 400
	else:
		pos = len(form.fields) + 1
		field = Field(form_id=form_id, fposition=pos, **data)
		field.save()
		field_dict = field.to_dict().copy()
		field_dict["company"] = "http://localhost:5000/api/v1/companies/{}".format(form.company.id)
		field_dict["form"] = "http://localhost:5000/api/v1/forms/{}".format(form_id)
		try:
				field_dict["options"] = eval(field.options)
		except:
					pass
		field_dict["uri"] = "http://localhost:5000/api/v1/fields/{}".format(field.id)
		return jsonify(field_dict), 201
	
@app_views.route('/fields/<field_id>', methods=['PUT'], strict_slashes=False)
def put_field(field_id):
	""" put field """
	field = storage.get(Field, field_id)
	if field is None:
		abort(404)
	data = request.get_json()
	if data is None:
		return 'Not a JSON data', 400
	field_dict["uri"] = "http://localhost:5000/api/v1/fields/{}".format(field.id)
	for key, value in data.items():
		if key not in ['id', 'created_at', 'updated_at']:
			setattr(field, key, value)
	field.save()
	field_dict = field.to_dict().copy()
	field_dict["company"] = "http://localhost:5000/api/v1/companies/{}".format(field.form.company.id)
	field_dict["form"] = "http://localhost:5000/api/v1/forms/{}".format(field.form.id)
	field_dict["uri"] = "http://localhost:5000/api/v1/fields/{}".format(field.id)
	return jsonify(field_dict), 200

@app_views.route('/fields/<field_id>', methods=['DELETE'], strict_slashes=False)
def delete_field(field_id):
	""" delete field """
	field = storage.get(Field, field_id)
	if field is None:
		abort(404)
	field.delete()
	return jsonify({}), 200
