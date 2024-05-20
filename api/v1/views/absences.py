#!/usr/bin/env python3

from flask import jsonify, request, abort, send_file
from api.v1.views import app_views
from models import storage, Absence, Employee
import pandas as pd
import io


@app_views.route('/employees/<employee_id>/absences', methods=['GET'])
def get_absences(employee_id):
    """Get absences for a given employee"""
    employee = storage.get(Employee, employee_id)
    if employee is None:
        abort(404)
    absences = [absence.to_dict() for absence in employee.absences]
    return jsonify(absences)

@app_views.route('/employees/<employee_id>/absences_sheet', methods=['GET'])
def get_absences_sheet(employee_id):
    """ Returns employee absences in excel sheet """
    employee = storage.get(Employee, employee_id)
    if employee is None:
        abort(404)
    absences = []
    for absence in employee.absences:
        absence_data = {
            "from": absence.start_date,
            "to": absence.end_date,
            "reason": absence.reason,
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

@app_views.route('/absences/<absence_id>', methods=['PUT'])
def update_absence(absence_id):
    """Update an absence"""
    reason = request.form.get('reason')
    if reason is None:
        abort(400, 'Reason missing')
    absence = storage.get(Absence, absence_id)
    if absence is None:
        abort(404)
    absence.reason = reason
    absence.save()
    return jsonify(absence.to_dict())