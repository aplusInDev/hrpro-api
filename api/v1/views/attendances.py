#!/usr/bin/env python3

from flask import jsonify, request, abort, send_file
from api.v1.views import app_views
from models import storage, Attendance, Company
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm.exc import NoResultFound
import io


@app_views.route("test", methods=['GET'])
def test():
    reqDate = request.args.get("date")
    return jsonify({"msg: ": "test", "date": reqDate})

@app_views.route('companies/<company_id>/attendance', methods=['POST'])
def post_employees_attendance(company_id):
    """ post employees attendance """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file:
        try:
            df = pd.read_excel(file, skiprows=1, usecols="B:F", names=[
                "date", "name", "check_in", "check_out", "absent"])
        except Exception as e:
            return jsonify({"post employee attendance error": str(e)}), 400
        for col in df.columns:
            df[col] = df[col].astype(str)
        # convert each row from str to datetime
        df['check_in'] = df['check_in'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "00:00:00")
        df['check_out'] = df['check_out'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "00:00:00")
        # for col in df.columns:
        #     df[col] = df[col].astype(str)
        df['absent'] = df['absent'].apply(lambda x: 'No' if x == "False" else 'Yes')
        
        # iterate over each row in the dataframe
        for index, row in df.iterrows():
            full_name = row["name"]
            full_name = full_name.split()
            if len(full_name) >= 2:
                first_name = full_name[0]
                last_name = " ".join(full_name[1:])
                print(first_name, last_name, sep="**")
            else:
                continue
            try:
                employee = storage.find_employee_by(first_name=first_name, last_name=last_name)
            except NoResultFound as err:
                print(err)
                continue

            if not employee:
                continue

            # check for redundancy
            existing_record = storage._session.query(Attendance).\
            filter_by(date=row['date'], employee_id=employee.id).first()
            if not existing_record:
                new_attendance = Attendance(
                    employee_id=employee.id , date=row['date'],
                    check_in=row['check_in'], check_out=row['check_out'],
                    absent=row['absent'],
                    )
                new_attendance.employee = employee
                new_attendance.save()
    
        return jsonify({"msg: ": "File uploaded successfully"}), 200
    return jsonify({"error: ": "No file part"}), 400

@app_views.route('companies/<company_id>/attendance', methods=['GET'])
def get_employees_attendance(company_id):
    """ get employees attendance """
    reqDate = request.args.get('date')
    # convert from str to date
    date = datetime.strptime(reqDate, '%Y-%m-%d').date()
    company = storage.get(Company, company_id)
    if company is None or reqDate is None:
        abort(404)

    print(date)
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
    df['duration'] = df.apply(lambda row: str(
            timedelta(seconds=(datetime.combine(date.min, row['check_out']) -
                               datetime.combine(date.min, row['check_in'])).\
                                total_seconds()) if row['absent'] == 'No'
                                else '0:00:00'
                                ),
                        axis=1)
    # for col in df.columns:
    #     df[col] = df[col].astype(str)
    # Create an in-memory buffer content as a send_file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    output.seek(0)  # Important: move to the beginning of the BytesIO buffer!

    # Return the buffer content as a 'send_file' response
    return send_file(
        output, download_name='book2.xlsx', as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.\
            spreadsheetml.sheet')
