#!/usr/bin/env pytho3
""" Test attendances view """

import unittest
from api.v1.app import app
from models import (
    storage, Employee, Company, Attendance,
)
from datetime import time, date
from uuid import uuid4
import pandas as pd
from flask import url_for
from io import BytesIO
from unittest.mock import patch


tm_format = "%Y-%m-%dT%H:%M:%S.%f"


class TestAttendanceView(unittest.TestCase):
    """ Test Attendance view """

    @classmethod
    def setUpClass(cls):
        """ SetUp for test """
        print('\n\n')
        print('.' * 50)
        print('... Test Absence class start ...')
        print('.' * 50)

    @classmethod
    def tearDownClass(cls) -> None:
        """ Test done """
        print('\n\n')
        print('.' * 50)
        print('... Test Absence class end ...')
        print('.' * 50)

    def setUp(self):
        """ set up for test """
        print('\n\n.................................')
        print('..... Test Attendance View .....')
        print('.................................')
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.name = str(uuid4())
        self.tm = time(8, 0, 0)
        self.dt = date.today().strftime("%Y-%m-%d")
        self.company = Company(name=self.name, address="testAddress")
        self.company.save()
        self.emp = Employee(
            first_name="John",
            last_name="Doe",
            company_id=self.company.id
        )
        self.emp.save()
        self.attendance_data = pd.DataFrame({
            'date': ['2021-01-01'],
            'name': ['John Doe'],
            'start_time': ['08:00:00'],
            'end_time': ['17:00:00'],
            'absent': ['False'],
        })
        self.attendance = Attendance(
            employee_id=self.emp.id,
            absent='No',
            date=self.dt,
            check_in=self.tm,
            check_out=self.tm,
        )
        self.attendance.save()

    def tearDown(self):
        """ remove test instances """
        try:
            storage.delete(self.emp)
        except Exception:
            pass
        print(".................................")
        print("..... End Test Attendance View .....")
        print(".................................")


    def test_attendance_instance(self):
        """ Test attendance instantiation """
        print('... Test attendance instantiation ...')
        self.assertIsInstance(self.attendance, Attendance)

    def test_attendance_instance_existance(self):
        """ Test attendance instance existance """
        print('... Test attendance instance existance ...')
        attendance = storage.get('Attendance', self.attendance.id)
        self.assertIsNotNone(attendance)

    def test_get_attendance_file(self):
        """ Test get attendance file """
        print('... Test get attendance file ...')
        year = date.today().year
        month = date.today().month
        with self.app.test_request_context():
            response = self.client.get(
                url_for('app_views.get_employee_attendance', employee_id=self.emp.id, year=year, month=month)
            )
            self.assertEqual(response.status_code, 200)
            self.assertTrue('book2.xlsx' in response.headers.get('Content-Disposition'))

    def test_company_instance(self):
        company = storage.get("Company", self.company.id)
        self.assertIsNotNone(company)
        
    def test_post_employees_attendance_async(self):
        """ Test post employees attendance async """
        print('... Test post employees attendance async ...')
        response = self.client.post('/companies/999/attendance_async', data={
            'file': (BytesIO(b'test data'), 'test.xlsx')
        })
        self.assertEqual(response.status_code, 404)

        # Test missing file part
        response = self.client.post('/companies/{}/attendance_async'.format(self.company.id))
        self.assertEqual(response.status_code, 404)
        self.assertIn('No file part', response.get_data(as_text=True))
