#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Attendance, Company
import pandas as pd
from datetime import datetime, date, timedelta

@app_views.route('/companies/<company_id>/attendance2', methods=['POST'])
def post_employees_attendance2(company_id):
    """Post employees attendance."""
    company = storage.get(Company, company_id)
    if not company:
        abort(404, description="Company not found.")

    file = request.files.get('file')
    if not file:
        return jsonify(error="No file provided."), 400

    try:
        df = pd.read_excel(file, skiprows=1, usecols="B:F", names=[
            "date", "name", "check_in", "check_out", "absent"])
    except Exception as e:
        return jsonify({"error": f"Failed to read Excel file: {e}"}), 400

    # Data cleaning and type conversion
    df.replace({'nan': None}, inplace=True)
    df['check_in'] = pd.to_datetime(df['check_in'], format='%H:%M:%S').dt.time
    df['check_out'] = pd.to_datetime(df['check_out'], format='%H:%M:%S').dt.time
    df['absent'] = df['absent'].map({'False': 'No', 'True': 'Yes'})

    # Calculate duration only for non-absent records
    df['duration'] = df.apply(
        lambda row: (datetime.combine(date.min, row['check_out']) - datetime.combine(date.min, row['check_in'])).total_seconds() / 3600
        if row['absent'] == 'No' else 0,
        axis=1
    )

    # Process each record
    for index, row in df.iterrows():
        first_name, last_name = row['name'].split()[:2]
        employee = storage.find_employee_by(first_name=first_name, last_name=last_name)

        if not employee:
            continue  # Skip if employee not found

        # Check for redundancy
        existing_record = storage._session.query(Attendance).filter_by(
            date=row['date'], employee_id=employee.id).first()

        if not existing_record:
            new_attendance = Attendance(
                employee_id=employee.id, date=row['date'],
                check_in=row['check_in'], check_out=row['check_out'],
                absent=row['absent'], duration=row['duration']
            )
            storage._session.add(new_attendance)

    storage._session.commit()  # Commit all new records at once
    return jsonify({"msg": "File uploaded and processed successfully"}), 200
