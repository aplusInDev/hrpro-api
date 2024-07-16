#!/usr/bin/env python3

from flask import jsonify, request, abort, send_file
from api.v1.views import app_views
from models import storage
import pandas as pd
import io


@app_views.route('/employees/<employee_id>/all_absences', methods=['GET'])
def get_absences(employee_id):
    """Get absences for a given employee"""
    employee = storage.get("Employee", employee_id)
    if employee is None:
        abort(404)
    absences = [absence.to_dict() for absence in employee.absences]
    return jsonify(absences)

@app_views.route(
        '/companies/<company_id>/employees_absences', methods=['GET'],
        strict_slashes=False)
def get_employees_absences(company_id):
    """ get employees """
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    year = request.args.get('year')
    if year is None:
        return jsonify({"error": "year is missing"}), 400
    employees_absences = []
    for employee in company.employees:
        employee_absences = storage.get_absences(employee.id, year)
        n_absences = len(employee_absences)
        absences_days = employee.calc_absences_days(year)
        justified_absences = employee.calc_justefied_absences(year)
        justified_days = employee.calc_justefied_absences_days(year)
        employees_absences.append({
            **employee.to_dict(),
            "absences_info": {
                "absences": n_absences,
                "absences_total_days": absences_days,
                "justified_absences": justified_absences,
                "justified_absences_days": justified_days,
                "unjustified_absences": n_absences - justified_absences,
                "unjustified_absences_days": absences_days - justified_days
            }
        })
    return jsonify(employees_absences)

@app_views.route('/employees/<employee_id>/absences_sheet', methods=['GET'])
def get_absences_sheet(employee_id):
    """ Returns employee absences in excel sheet """
    employee = storage.get("Employee", employee_id)
    year = request.args.get('year')
    if employee is None or not year:
        abort(404)
    absences = []
    employee_absences = storage.get_absences(employee_id, year)
    for absence in employee_absences:
        absence_dict = absence.to_dict().copy()
        absence_data = {
            "from": absence_dict["start_date"],
            "to": absence_dict["end_date"],
            "reason": absence_dict["reason"],
            "n_days": str(absence_dict["n_days"]),
        }
        absences.append(absence_data)
    df = pd.DataFrame(absences)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    output.seek(0)  # Important: move to the beginning of the BytesIO buffer!

    return send_file(
        output, download_name='book2.xlsx', as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.\
            spreadsheetml.sheet'), 200

@app_views.route('/employees/<employee_id>/absences', methods=['GET'])
def get_employee_absences(employee_id: str) -> list:
    """Get absences for a given employee based on giving year
    Args:
        employee_id: the id of the employee
        year: absences year
    Returns:
        list of absences based on giving year
    """
    employee = storage.get("Employee", employee_id)
    if employee is None:
        abort(404)
    year = request.args.get('year')
    if year is None:
        return jsonify({"error": "year is missing"}), 400
    absences = storage.get_absences(employee_id, year)
    absences_res = []
    for absence in absences:
        absence_dict = absence.to_dict().copy()
        absence_data = {
            "id": absence_dict["id"],
            "from": absence_dict["start_date"],
            "to": absence_dict["end_date"],
            "reason": absence_dict["reason"] if absence_dict["reason"] else "",
            "n_days": absence_dict["n_days"],
        }
        absences_res.append(absence_data)
    return jsonify(absences_res)

@app_views.route('/absences/<absence_id>', methods=['PUT'])
def update_absence(absence_id):
    """Update an absence"""
    reason = request.json.get('reason')
    if reason is None:
        abort(400, 'Reason missing')
    absence = storage.get("Absence", absence_id)
    if absence is None:
        abort(404)
    absence.reason = reason
    absence.save()
    return jsonify(absence.to_dict())
