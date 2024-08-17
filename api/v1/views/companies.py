#!/usr/bin/env python3
""" companies views """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from api.v1.auth.middleware import requires_auth
from api.v1.utils.auth_utils import verify_account_company_id


@app_views.route('/companies/<company_id>', methods=['GET'], strict_slashes=False)
@requires_auth()
def get_company(company_id):
    """ get company """
    session_id = request.cookies.get('session_id')
    if not verify_account_company_id(session_id, company_id):
        abort(403)
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    return jsonify(company.to_dict())


@app_views.route('/companies/<company_id>', methods=['PUT'], strict_slashes=False)
@requires_auth(["admin"])
def put_company(company_id):
    """ put company """
    session_id = request.cookies.get('session_id')
    if not verify_account_company_id(session_id, company_id):
        abort(403)
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    data = request.form.to_dict()
    if data is None:
        return 'Not a JSON', 400
    for key, value in data.items():
        if key not in [
            'id', 'created_at', 'updated_at', 'forms',
            'employees', 'jobs', 'departments'
        ]:
            setattr(company, key, value)
    company.save()
    return jsonify(company.to_dict())
