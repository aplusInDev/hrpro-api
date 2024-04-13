#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Employee, Absence


@app_views.route('/employees/<employee_id>/absences', methods=['GET'], strict_slashes=False)
def get_absences(employee_id):
    """ get absences """
    employee = storage.get(Employee, employee_id)
    if employee is None:
        abort(404)
    all_absences = [absence.to_dict() for absence in employee.absences]
    return jsonify(all_absences)


@app_views.route('/absences/<absence_id>', methods=['GET'], strict_slashes=False)
def get_absence(absence_id):
    """ get absence """
    absence = storage.get(Absence, absence_id)
    if absence is None:
        abort(404)
    return jsonify(absence.to_dict())


@app_views.route('/employees/<employee_id>/absences', methods=['POST'], strict_slashes=False)
def post_absence(employee_id):
    """ post absence """
    employee = storage.get(Employee, employee_id)
    if employee is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'start_date' not in data or 'end_date' not in data:
        return 'Absence informations missing', 400
    absence = Absence(**data)
    absence.employee_id = employee_id
    absence.save()
    return jsonify(absence.to_dict()), 201


@app_views.route('/absences/<absence_id>', methods=['PUT'], strict_slashes=False)
def put_absence(absence_id):
    """ put absence """
    absence = storage.get(Absence, absence_id)
    if absence is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(absence, key, value)
    absence.save()
    return jsonify(absence.to_dict())


@app_views.route('/absences/<absence_id>', methods=['DELETE'], strict_slashes=False)
def delete_absence(absence_id):
    """ delete absence """
    absence = storage.get(Absence, absence_id)
    if absence is None:
        abort(404)
    absence.delete()
    return jsonify({}), 200
