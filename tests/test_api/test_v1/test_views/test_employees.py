#!/usr/bin/env python3
""" Test employees view """

import unittest
from api.v1.app import app
from models import (
    storage, Employee, Company,
    Department, Job,
)
from uuid import uuid4


class TestEmployeeView(unittest.TestCase):
    """ Test Employee view """
    def setUp(self):
        """ set up for test """
        print('\n\n.................................')
        print('..... Test Employee View .....')
        print('.................................\n\n')
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.name = str(uuid4())
        self.company = Company(name=self.name, address="testAddress")
        self.company.save()
        self.emp = Employee(first_name="John", last_name="Doe")
        self.emp.save()
        self.dep = Department(name=self.name, company_id=self.company.id)
        self.dep.save()
        self.job = Job(title=self.name, company_id=self.company.id)
        self.job.save()

    def tearDown(self):
        """ remove test instances """
        try:
            storage.delete(self.emp)
        except Exception:
            pass
        print(".................................\n\n")
        print("..... End Test Employee View .....\n\n")
        print(".................................\n\n")

    def test_company_id(self):
        """ Test compnay id existance """
        print("... Test company id existance ...")
        self.assertIsNotNone(self.company.id)

    def test_company_instance(self):
        """ Test company instantiation """
        print('... Test company instantiation ...')
        self.assertIsInstance(self.company, Company)

    def test_company_instance_existance(self):
        """ Test company instance existance """
        print('... Test company instance existance ...')
        company = storage.get('Company', self.company.id)
        self.assertIsNotNone(company)

    def test_department_id(self):
        """ Test deparmtnet id existance """
        print("... Test department id existance ...")
        self.assertIsNotNone(self.dep.id)

    def test_department_instance(self):
        """ Test department instantiation """
        print('... Test department instantiation ...')
        self.assertIsInstance(self.dep, Department)
    
    def test_department_instance_existance(self):
        """ Test department instance existance """
        print('... Test department instance existance ...')
        department = storage.get('Department', self.dep.id)
        self.assertIsNotNone(department)

    def test_job_id(self):
        """ Test job id existance """
        print("... Test job id existance ...")
        self.assertIsNotNone(self.job.id)

    def test_job_instance(self):
        """ Test job instantiation """
        print('... Test job instantiation ...')
        self.assertIsInstance(self.job, Job)

    def test_job_instance_existance(self):
        """ Test job instance existance """
        print('... Test job instance existance ...')
        job = storage.get('Job', self.job.id)
        self.assertIsNotNone(job)

    def test_get_employees(self):
        """ Test get employees """
        print('... Test GET/ employees ...')
        response = self.client.get(
            '/api/v1/companies/{}/employees'.format(self.company.id))
        self.assertEqual(response.status_code, 200)

    def test_get_employee(self):
        """ Test get employee """
        print('... Test GET/ employees/<employee_id> ...')
        response = self.client.get('/api/v1/employees/{}'.format(self.emp.id))
        self.assertEqual(response.status_code, 200)

    def test_post_employee(self):
        """ Test post employee """
        print('... Test POST/ add_employee ...')
        response = self.client.post(
            '/api/v1/add_employee?company_id={}'.format(self.company.id),
            data={
                "first_name": "janedoe",
                "last_name": "janedoe1",
                "email": "hrpro.team2024@gmail.com",
                "department": self.dep.name,
                "job_title": self.job.title,
        })
        self.assertEqual(response.status_code, 202)

    # def test_post_employee_return_type(self):
    #     """ Test post employee return type """
    #     print('... Test POST/ add_employee return type ...')
    #     response = self.client.post(
    #         '/api/v1/add_employee?company_id={}'.format(self.company.id),
    #         data={
    #             "first_name": "janedoe",
    #             "last_name": "janedoe2",
    #             "email": "hrpro.team2024@gmail.com",
    #             "department": self.dep.name,
    #             "job_title": self.job.title,
    #     })
    #     self.assertIsInstance(response.json, dict)

    # def test_post_employee_return(self):
    #     """ Test post employee return """
    #     print('... Test POST/ add_employee return ...')
    #     response = self.client.post(
    #         '/api/v1/add_employee?company_id={}'.format(self.company.id),
    #         data={
    #             "first_name": "janedoe",
    #             "last_name": "janedoe3",
    #             "email": "hrpro.team2024@gmail.com",
    #             "department": self.dep.name,
    #             "job_title": self.job.title,
    #     })
    #     response_data = response.json
    #     self.assertIn('first_name', response_data)
    #     self.assertIn('last_name', response_data)
    #     self.assertIn('info', response_data)

    def test_put_employee(self):
        """ Test put employee """
        response = self.client.put('/api/v1/employees/{}'.format(self.emp.id), json={
            "first_name": "Jane",
            "last_name": "Doe"
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_employee(self):
        """ Test delete employee """
        response = self.client.delete('/api/v1/employees/{}'.format(self.emp.id))
        self.assertEqual(response.status_code, 204)