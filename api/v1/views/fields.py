#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Field


@app_views.route('forms/<form_id>/fields', methods=['GET'], strict_slashes=False)
def get_fields(form_id):
	""" get fields """
	form = storage.get("Form", form_id)
	if form is None:
		abort(404)
	return jsonify([field.to_dict() for field in form.fields])

@app_views.route('fields', methods=['GET'], strict_slashes=False)
def get_form_fields():
	"""Get all form fields based on form name and company_id
	"""
	form_name = request.args.get('form_name')
	company_id = request.args.get('company_id')
	if not form_name:
		return jsonify({'error': 'Missing form_name'}), 400
	if not company_id:
		return jsonify({'error': 'Missing company_id'}), 400
	form = storage.find_form_by_(name=form_name, company_id=company_id)
	return get_fields(form.id)

@app_views.route('/fields/<field_id>', methods=['GET'], strict_slashes=False)
def get_field(field_id):
	""" get field """
	field = storage.get("Field", field_id)
	if field is None:
		abort(404)
	return jsonify(field.save())

@app_views.route('/forms/<form_id>/fields', methods=['POST'], strict_slashes=False)
def post_field(form_id):
	""" post field """
	form = storage.get("Form", form_id)
	if form is None:
		abort(404)
	data = request.get_json()
	if data is None:
		return jsonify({'error': 'Not a JSON data'}), 400
	elif 'name' not in data:
		return jsonify({'error': 'Missing field name'}), 400
	else:
		field_name = data['name']
		field = storage.find_field_by(
			name=field_name,
			form_id=form_id,
		)
		if field:
			return jsonify({
				"error": "{} Field already exists".format(field_name)
			}), 400
		if 'options' in data:
			options = eval(data['options'])
			options = list(set(options))
			data['options'] = str(options)
		field = Field(form_id=form_id, **data)
		field.save()
		return jsonify(field.to_dict()), 201
	
@app_views.route('/fields/<field_id>', methods=['PUT'], strict_slashes=False)
def put_field(field_id):
	""" put field """
	field = storage.get("Field", field_id)
	if field is None:
		abort(404)
	data = request.get_json()
	if data is None:
		return 'Not a JSON data', 400
	for key, value in data.items():
		if key not in ['id', 'created_at', 'updated_at']:
			setattr(field, key, value)
	field.save()
	return jsonify(field.save()), 200

@app_views.route('/fields/<field_id>', methods=['DELETE'], strict_slashes=False)
def delete_field(field_id):
	""" delete field """
	field = storage.get("Field", field_id)
	if field is None:
		abort(404)
	field.delete()
	return jsonify({}), 200
