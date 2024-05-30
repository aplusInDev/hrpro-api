#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Leave
from api.v1.auth.middleware import requires_auth


@app_views.route('/leaves', methods=['GET'], strict_slashes=False)
@requires_auth(["admin", "hr"])
def get_leaves():
    """ get leaves view
    return all leaves for each employee in the company
    based on the giving year
    Args:
        company_id: the id of the company
        year: the year of the leaves
    """
    required_args = ['company_id', 'year']
    for arg in required_args:
        if arg not in request.args.to_dict():
            return jsonify({"error": f"{arg} is required"}), 400
    company_id = request.args.get("company_id")
    year = request.args.get("year")
    leaves = storage.get_leaves(company_id, year)
    return jsonify(leaves)

@app_views.route('/employees/<employee_id>/leaves', methods=['GET'], strict_slashes=False)
@requires_auth()
def get_employee_leaves(employee_id):
    """ get leaves view
    return all leaves for each employee in the company
    based on the giving year
    Args:
        company_id: the id of the company
        year: the year of the leaves
    """
    employee = storage.get("Employee", employee_id)
    if not employee:
        return jsonify({"error": "employee not found"}), 404
    return jsonify([leave.to_dict() for leave in employee.leaves])

@app_views.route('/employees/<employee_id>/leaves', methods=['POST'], strict_slashes=False)
@requires_auth()
def create_leave(employee_id):
    """ create leave view
    create a new leave for an employee
    Args:
        start_date: the start date of the leave
        end_date: the end date of the leave
        leave_type: the type of the leave
        reason: (optional) the reason of the leave
    """
    employee = storage.get("Employee", employee_id)
    if not employee:
        return jsonify({"error": "employee not found"}), 404
    required_fileds = ['start_date', 'end_date', 'leave_type']
    for field in required_fileds:
        if field not in request.form.to_dict():
            return jsonify({"error": f"{field} is required"}), 400
    data = request.form.to_dict()
    leave = Leave(**data, employee_id=employee_id)
    leave.save()
    return jsonify(leave.to_dict()), 201

@app_views.route('/leaves/<leave_id>', methods=['PUT'], strict_slashes=False)
@requires_auth(["admin", "hr"])
def update_leave(leave_id):
    """ update leave view
    update a leave status
    Args:
        status: the new status of the leave
    """
    leave = storage.get("Leave", leave_id)
    if not leave:
        return jsonify({"error": "leave not found"}), 404
    data = request.get_json()
    if not data or "status" not in data:
        return jsonify({"error": "status is required"}), 400
    leave.status = data["status"]
    leave.save()
    return jsonify(leave.to_dict())
