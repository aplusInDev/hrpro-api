from sqlalchemy.orm.exc import NoResultFound
from models import storage, Attendance
import asyncio


def handle_attendance_sync(df):
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

async def handle_attendance(df):
    tasks = []
    for index, row in df.iterrows():
        task = asyncio.create_task(process_employee_attendance(row))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def process_employee_attendance(row):
    full_name = row["name"]
    full_name = full_name.split()
    if len(full_name) >= 2:
        first_name = full_name[0]
        last_name = " ".join(full_name[1:])
    else:
        return

    try:
        employee = storage.find_employee_by(first_name=first_name, last_name=last_name)
    except NoResultFound as err:
        print(err)
        return

    if not employee:
        return

    # check for redundancy
    existing_record = storage._session.query(Attendance). \
        filter_by(date=row['date'], employee_id=employee.id).first()
    if not existing_record:
        new_attendance = Attendance(
            employee_id=employee.id, date=row['date'],
            check_in=row['check_in'], check_out=row['check_out'],
            absent=row['absent'],
        )
        new_attendance.employee = employee
        new_attendance.save()
