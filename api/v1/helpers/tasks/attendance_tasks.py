from api.celery_app import celery_app
from sqlalchemy.orm.exc import NoResultFound
from models import storage, Attendance, Absence
import pandas as pd
import asyncio


@celery_app.task
def handle_attendance_async(company_id: str, df_json) -> str:
    """
    A Celery task that processes employee attendance records asynchronously.

    This function is designed to be queued as a background job and handles the processing of attendance data for all employees
    in a company. It takes a JSON string representing a DataFrame of attendance records, converts it back into a DataFrame,
    and then asynchronously processes each row using the `process_employee_attendance` function.

    Parameters:
    - company_id (str): The unique identifier for the company.
    - df_json (str): A JSON string representing the DataFrame of attendance records.

    Returns:
    - str: A message indicating the completion status of the task.
    """
    # Convert JSON string back to DataFrame
    df = pd.read_json(df_json, orient='split')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            *(process_employee_attendance(company_id, row) for index, row in df.iterrows())
        )
    )
    return "Task done successfully"

async def process_employee_attendance(company_id: str, row) -> None:
    """
    Asynchronously processes an employee's attendance record for a given day.

    This function takes a company ID and a row of attendance data, then attempts to find an employee
    matching the name provided in the row within the specified company. If the employee is found,
    the function checks for an existing attendance record for that date. If no record exists, it creates
    a new attendance record with the provided data. If the employee was absent, it either creates a new
    absence record or updates the existing one using the `process_employee_absence` function.

    Parameters:
    - company_id (str): The unique identifier for the company.
    - row (dict): A dictionary containing attendance data with keys for 'name', 'date', 'check_in', 'check_out', and 'absent'.

    Returns:
    - None
    """
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
        print("request error (No result found)", err)
        return

    if not employee:
        return

    # check for redundancy
    existing_record = storage._session.query(Attendance).\
        filter_by(date=row['date'], employee_id=employee.id).first()
    if existing_record:
        return
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

async def process_employee_absence(employee, absence_date: str) -> None:
    """
    Asynchronously processes an employee's absence for a given date.

    This function checks if the provided absence date falls within any existing absence periods for the employee.
    If it does, the function exits without making any changes. If the absence date is after the latest absence period,
    it checks the employee's latest attendance record. If the employee was marked absent on their last recorded attendance,
    the function updates the end date of the current absence period to the provided absence date. If there are no overlapping
    absences and the employee was not absent on their last attendance day, a new absence record is created for the absence date.

    Parameters:
    - employee (Employee): The employee object containing absence information.
    - absence_date (str): The date of absence to process, in 'YYYY-MM-DD' format.

    Returns:
    - None
    """
    employee_absences = [absence.to_dict() for absence in employee.absences]
    df = pd.DataFrame(employee_absences)
    
    # Convert 'start_date' and 'end_date' to Timestamps
    # to solve the comparison between string and Timestamp objects issue
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    
    # Ensure 'absence_date' is a Timestamp
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
