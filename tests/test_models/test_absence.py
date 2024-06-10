#!/usr/bin/env python3
""" Test absence model """


import unittest
from models import Employee, storage, Absence
from datetime import datetime
from uuid import uuid4


tm_format = "%Y-%m-%dT%H:%M:%S.%f"

class TestAbsence(unittest.TestCase):
    """ Test Absence class """

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
        self.id = uuid4()
        self.first_name = "John"
        self.last_name = "Doe"
        self.created_at = datetime.now().strftime(tm_format)
        self.updated_at = datetime.now().strftime(tm_format)
        self.emp = Employee(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        self.emp.save()
        self.abs = Absence(
            employee_id=self.id,
            create_at=self.created_at,
            updated_at=self.updated_at,
            start_date=self.created_at,
            end_date=self.created_at,
        )
        self.abs.save()

    def tearDown(self):
        """ remove test instances """
        del self.emp

    def test_not_None_amployee(self):
        """ Test if employee instance is not None """
        print("... Test if employee instance is not None  ...")
        self.assertIsNotNone(self.emp)

    def test_not_None_absence(self):
        """ Test if absence instance is not None """
        print("... Test if absence instance is not None ...")
        self.assertIsNotNone(self.abs)

    def test_get_nont_None_abs_return(self):
        """ Test storage get method """
        print("... Test storage get method for absence instance, " +
              "the result should not be None...")
        abs = storage.get("Absence", self.abs.id)
        self.assertIsNotNone(abs)

    def test_get_correct_instantiation_return(self):
        """ Test storage get method """
        print("... Test storage get method for an absence instance, " +
              "the result should equals to the absence instance ...")
        abs = storage.get("Absence", self.abs.id)
        self.assertIsInstance(abs, Absence)
    
    def test_get_correct_return(self):
        """ Test storage get method """
        print("... Test for correct instance return ...")
        abs = storage.get("Absence", self.abs.id)
        self.assertEqual(abs, self.abs)
