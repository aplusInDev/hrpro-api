from api.celery_app import app
from sqlalchemy.orm.exc import NoResultFound
from models import storage, Attendance, Absence
from datetime import datetime
import pandas as pd
import asyncio


@app.task
def handle_attendance_async(company_id, df_json):
    # Convert JSON string back to DataFrame
    df = pd.read_json(df_json, orient='split')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            *(process_employee_attendance(company_id, row) for index, row in df.iterrows())
        )
    )

async def process_employee_attendance(company_id, row):
    full_name = row["name"]
    full_name = full_name.split()
    if len(full_name) >= 2:
        first_name = full_name[0]
        last_name = " ".join(full_name[1:])
    else:
        return

    try:
        employee = storage.find_employee_by(
            first_name=first_name,
            last_name=last_name,
            company_id=company_id,
        )
    except NoResultFound as err:
        # print("request error (No result found)", err)
        return

    if not employee:
        return

    # check for redundancy
    existing_record = storage._session.query(Attendance).\
        filter_by(date=row['date'], employee_id=employee.id).first()
    if not existing_record:
        new_attendance = Attendance(
            employee_id=employee.id, date=row['date'],
            check_in=row['check_in'], check_out=row['check_out'],
            absent=row['absent'],
        )
        if row['absent'] == 'Yes':
            if len(employee.absences) == 0:
                new_absence = Absence(
                    employee_id=employee.id, start_date=row['date'],
                    end_date=row['date']
                )
                new_absence.employee = employee
                new_absence.save()
            else:
                # process_employee_absence(employee, row['date'])
                asyncio.create_task(process_employee_absence(employee, row['date']))
        new_attendance.employee = employee
        new_attendance.save()

async def process_employee_absence(employee, absence_date):
    """ process employee absence  """
    employee_absences = [absence.to_dict() for absence in employee.absences]
    df = pd.DataFrame(employee_absences)
    absence_date = pd.Timestamp(absence_date)
    df.sort_values(by='start_date', inplace=True, ascending=False)
    for index, row in df.iterrows():
        if row['start_date'] <= absence_date <= row['end_date']:
            return
        if row['start_date'] < absence_date:
            latest_attendance = storage._session.query(Attendance).\
                filter(Attendance.employee_id == employee.id,
                          Attendance.date < absence_date).\
                order_by(Attendance.date.desc()).first()
            if latest_attendance and latest_attendance.absent == 'Yes':
                try:
                    current_absence = storage._session.query(Absence).\
                        filter(Absence.id == row['id']).first()
                    current_absence.end_date = absence_date
                    current_absence.save()
                    return
                except NoResultFound:
                    return
            new_absence = Absence(
                employee_id=employee.id, start_date=absence_date,
                end_date=absence_date
            )
            new_absence.employee = employee
            new_absence.save()
            return
