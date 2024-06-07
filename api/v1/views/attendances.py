#!/usr/bin/env python3

from flask import jsonify, request, abort, send_file
from api.v1.views import app_views
from models import storage
from datetime import datetime, timedelta, date
from api.v1.helpers import handle_attendance_sync, handle_attendance
import pandas as pd
import io


@app_views.route('companies/<company_id>/attendance_sync', methods=['POST'])
def post_employees_attendance_sync(company_id):
    """ post employees attendance """
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file:
        try:
            df = pd.read_excel(file, skiprows=1, usecols="B:F", names=[
                "date", "name", "check_in", "check_out", "absent"])
            for col in df.columns:
                df[col] = df[col].astype(str)
            # convert each row from str to datetime
            df['check_in'] = df['check_in'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "00:00:00")
            df['check_out'] = df['check_out'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "00:00:00")
            # for col in df.columns:
            #     df[col] = df[col].astype(str)
            df['absent'] = df['absent'].apply(lambda x: 'No' if x == "False" else 'Yes')
        except Exception as e:
            return jsonify({"post employee attendance error": str(e)}), 400
        handle_attendance_sync(df)
        return jsonify({"msg: ": "File uploaded successfully"}), 200

@app_views.route('companies/<company_id>/attendance_async', methods=['POST'])
async def post_employees_attendance_async(company_id):
    """ post employees attendance """
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    if 'file' not in request.files:
        return 'No file part', 400
    if 'file' not in request.files:
        return jsonify({"error: ": "No file part"}), 400
    file = request.files['file']
    if file:
        try:
            df = pd.read_excel(file, skiprows=1, usecols="B:F", names=[
                "date", "name", "check_in", "check_out", "absent"])

            for col in df.columns:
                df[col] = df[col].astype(str)
            # convert each row from str to datetime
            df['check_in'] = df['check_in'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "00:00:00")
            df['check_out'] = df['check_out'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "00:00:00")
            df['absent'] = df['absent'].apply(lambda x: 'No' if x == "False" else 'Yes')
        except Exception as e:
            return jsonify({"error": "file structure should be like " +
                            "column_B => date(date), column_B => name(string)" +
                            ", column_C => check_in(time), column_D => " +
                            "check_out(time) , column_E => " +
                            "absent(TRUE | FALSE)"}), 400
        await handle_attendance(df)
        return jsonify({"msg: ": "File uploaded successfully"}), 200

@app_views.route('companies/<company_id>/attendance', methods=['POST'])
def post_employees_attendance(company_id):
    """ post employees attendance """
    company = storage.get("Company", company_id)
    if company is None:
        abort(404)
    if 'file' not in request.files:
        return 'No file part', 400
    if 'file' not in request.files:
        return jsonify({"error: ": "No file part"}), 400
    file = request.files['file']
    if file:
        try:
            df = pd.read_excel(file, skiprows=1, usecols="B:F", names=[
                "date", "name", "check_in", "check_out", "absent"])

            for col in df.columns:
                df[col] = df[col].astype(str)
            # convert each row from str to datetime
            df['check_in'] = df['check_in'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "00:00:00")
            df['check_out'] = df['check_out'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "00:00:00")
            df['absent'] = df['absent'].apply(lambda x: 'No' if x == "False" else 'Yes')
        except Exception as e:
            return jsonify({"error": "file structure should be like " +
                            "column_B => date(date), column_B => name(string)" +
                            ", column_C => check_in(time), column_D => " +
                            "check_out(time) , column_E => " +
                            "absent(TRUE | FALSE)"}), 400
        # process_attendance_data(company_id, df)
        return jsonify({"msg: ": "File uploaded successfully"}), 200

@app_views.route('companies/<company_id>/attendance', methods=['GET'])
def get_employees_attendance(company_id):
    """ get employees attendance """
    reqDate = request.args.get('date')
    # convert from str to date
    date = datetime.strptime(reqDate, '%Y-%m-%d').date()
    company = storage.get("Company", company_id)
    if company is None or reqDate is None:
        abort(404)

    attendances = []
    for employee in company.employees:
        for attendance in employee.attendances:
            if attendance.date == date:
                attendance_data = {
                    "date": attendance.date,
                    "employee_name": f"{employee.first_name} {employee.last_name}",
                    "check_in": attendance.check_in,
                    "check_out": attendance.check_out,
                    "absent": attendance.absent,
                }
                attendances.append(attendance_data)

    df = pd.DataFrame(attendances)
    if len(attendances) != 0:
        df['duration'] = df.apply(lambda row: str(
                timedelta(seconds=(datetime.combine(date.min, row['check_out']) -
                                datetime.combine(date.min, row['check_in'])).\
                                    total_seconds()) if row['absent'] == 'No'
                                    else '0:00:00'
                                    ),
                            axis=1)

    # Create an in-memory buffer content as a send_file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    output.seek(0)  # Important: move to the beginning of the BytesIO buffer!

    if len(attendances) == 0:
        return send_file(
            output, download_name='book2.xlsx', as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.\
                spreadsheetml.sheet'), 404

    return send_file(
        output, download_name='book2.xlsx', as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.\
            spreadsheetml.sheet'), 200

@app_views.route('/employees/<employee_id>/attendance', methods=['GET'])
def get_employee_attendance(employee_id):
    """ retrieve employee attendance
    Args:
        employee_id: the id of the employee
        year: attendance year
        month: attendance month
    Returns:
        list of attendances based on giving month and year
    """
    employee = storage.get("Employee", employee_id)
    if not employee:
        return jsonify({"error": "employee not found"}), 404
    required_fileds = ["month", "year"]
    for field in required_fileds:
        if field not in request.args:
            return jsonify({"error": f"{field} is required"}), 400
    year = request.args.get("year")
    month = request.args.get("month")
    attendances = storage.get_attendances(employee_id, year, month)
    attendances_result = []
    for attendance in attendances:
        attendance_data = {
                    "date": attendance.date,
                    "check_in": attendance.check_in,
                    "check_out": attendance.check_out,
                    "absent": attendance.absent,
                }
        attendances_result.append(attendance_data)
    df = pd.DataFrame(attendances_result)
    if len(attendances_result) != 0:
        df['duration'] = df.apply(lambda row: str(
                timedelta(seconds=(datetime.combine(date.min, row['check_out']) -
                                datetime.combine(date.min, row['check_in'])).\
                                    total_seconds()) if row['absent'] == 'No'
                                    else '0:00:00'
                                    ),
                            axis=1)

    # Create an in-memory buffer content as a send_file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    output.seek(0)  # Important: move to the beginning of the BytesIO buffer!

    return send_file(
        output, download_name='book2.xlsx', as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.\
            spreadsheetml.sheet')
