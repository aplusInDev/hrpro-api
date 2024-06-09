#!/usr/bin/env python3
""" Test module for the Employee class """

import unittest
from models import Employee, storage
from datetime import datetime

class TestEmployee(unittest.TestCase):
    """ Test Employee class """
    def setUp(self):
        """ set up for test """
        print('\n\n.................................')
        print('..... Test Employee Class .....')
        self.first_name = "John"
        self.last_name = "Doe"
        self.emp = Employee(first_name=self.first_name, last_name=self.last_name)
        self.emp.save()
        self.id = self.emp.id
        self.created_at = self.emp.created_at
        self.updated_at = self.emp.updated_at

    def tearDown(self):
        """ remove test instances """
        del self.emp
        print(".................................\n\n")
        print("..... End Test Employee Class .....\n\n")
        print(".................................\n\n")

    def test_instance(self):
        """ Test if instance of Employee """
        print('... Testing instance of Employee ...')
        self.assertIsInstance(self.emp, Employee)

    def test_id_type(self):
        """ Test if id type str """
        print('... Testing if id type of str ...')
        self.assertIsInstance(self.emp.id, str)

    def test_created_at_type(self):
        """ Test created_at type  """
        print('... Testing if created_at is datetime type ...')
        self.assertIsInstance(self.emp.created_at, datetime)

    def test_correct_created_at(self):
        """ Test correct created_at of Employee"""
        print('... Test for correct created_at ...')
        self.assertEqual(self.created_at, self.emp.created_at)

    def test_updated_at(self):
        """ Test updated_at of Employee"""
        print('... Test updated_at of Employee ...')
        self.assertIsInstance(self.emp.updated_at, datetime)

    def test_first_name(self):
        """ Test first_name type """
        print("""... Test first_name attr type ...""")
        self.assertIsInstance(self.emp.first_name, str)

    def test_correct_first_name(self):
        """ Test correct first_name """
        print("... Test correct first_name ...")
        self.assertEqual(self.first_name, self.emp.first_name)

    def test_last_name(self):
        """ Test last_name type """
        print("... Test last_name attr type ...")
        self.assertIsInstance(self.emp.last_name, str)

    def test_correct_last_name(self):
        """ Test correct last_name """
        print("... Test correct last_name ...")
        self.assertEqual(self.last_name, self.emp.last_name)

    def test_to_dict(self):
        """ Test to_dict method """
        print('... Testing to_dict method of Employee ...')
        emp_dict = self.emp.to_dict()
        self.assertIsInstance(emp_dict, dict)
        self.assertEqual(emp_dict['__class__'], 'Employee')
        self.assertEqual(emp_dict['id'], self.id)
        self.assertEqual(emp_dict['created_at'], self.created_at.isoformat())
        self.assertEqual(emp_dict['updated_at'], self.updated_at.isoformat())

    def test_save(self):
        """ Test save method """
        print('... Testing save method of Employee ...')
        self.emp.save()
        self.assertNotEqual(self.updated_at, self.emp.updated_at)

    def test_get_nont_None_return(self):
        """ Test storage get method """
        print("... Test storage get method for employee instance,\
              the result should not be None...")
        emp = storage.get("Employee", self.id)
        self.assertIsNotNone(emp)

    def test_get_correct_instantiation_return(self):
        """ Test storage get method """
        print("... Test storage get method for an employee instance,\
              the result should equals to the employee instance ...")
        emp = storage.get("Employee", self.id)
        self.assertIsInstance(emp, Employee)
    
    def test_get_correct_return(self):
        """ Test storage get method """
        print("... Test for correct instance return ...")
        emp = storage.get("Employee", self.id)
        self.assertEqual(emp, self.emp)
  
