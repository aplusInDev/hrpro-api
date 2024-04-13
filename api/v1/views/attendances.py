#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Employee, Attendance


@app_views.route('/employees/<employee_id>/attendances', methods=['GET'], strict_slashes=False)
def get_attendances(employee_id):
    """ get attendances """
    employee = storage.get(Employee, employee_id)
    if employee is None:
        abort(404)
    all_attendances = [attendance.to_dict() for attendance in employee.attendances]
    return jsonify(all_attendances)

@app_views.route('/attendances/<attendance_id>', methods=['GET'], strict_slashes=False)
def get_attendance(attendance_id):
    """ get attendance """
    attendance = storage.get(Attendance, attendance_id)
    if attendance is None:
        abort(404)
    return jsonify(attendance.to_dict())

@app_views.route('/employees/<employee_id>/attendances', methods=['POST'], strict_slashes=False)
def post_attendance(employee_id):
    """ post attendance """
    employee = storage.get(Employee, employee_id)
    if employee is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'check_in' not in data or 'check_out' not in data:
        return 'Attendance informations missing', 400
    attendance = Attendance(**data)
    attendance.employee_id = employee_id
    attendance.save()
    return jsonify(attendance.to_dict()), 201

@app_views.route('/attendances/<attendance_id>', methods=['PUT'], strict_slashes=False)
def put_attendance(attendance_id):
    """ put attendance """
    attendance = storage.get(Attendance, attendance_id)
    if attendance is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(attendance, key, value)
    attendance.save()
    return jsonify(attendance.to_dict())

@app_views.route('/attendances/<attendance_id>', methods=['DELETE'], strict_slashes=False)
def delete_attendance(attendance_id):
    """ delete attendance """
    attendance = storage.get(Attendance, attendance_id)
    if attendance is None:
        abort(404)
    attendance.delete()
