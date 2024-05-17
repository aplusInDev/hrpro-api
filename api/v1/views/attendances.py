#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Department, Company
import pandas as pd
from datetime import datetime, date, timedelta

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
        df = pd.read_excel(file, skiprows=1, usecols="B:F", names=[
            "date", "name", "check_in", "check_out", "absent"])
        for col in df.columns:
            df[col] = df[col].astype(str)
        # convert each row from str to datetime
        df['check_in'] = df['check_in'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "nan")
        df['check_out'] = df['check_out'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "nan")
        df['duration'] = df.apply(lambda row: str(
            timedelta(seconds=(datetime.combine(date.min, row['check_out']) -
                                 datetime.combine(date.min, row['check_in'])).\
                                total_seconds()) if row['absent'] != 'True'
                                else '0:00:00'
                                ),
                        axis=1)
        for col in df.columns:
            df[col] = df[col].astype(str)
        df['absent'] = df['absent'].apply(lambda x: 'No' if x == "False" else 'Yes')
        # return jsonify(df.to_dict(orient='records')), 200
    
        return jsonify({"msg": "File uploaded successfully"}), 200
    return jsonify({"error": "Not a form data"}), 400
