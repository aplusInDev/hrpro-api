#!/usr/bin/env python3
""" Test module for the BaseModel class """

import unittest
from models import BaseModel
from datetime import datetime

class TestBaseModel(unittest.TestCase):
    """ Test BaseModel class """
    def setUp(self):
        """ set up for test """
        print('\n\n.................................')
        print('..... Test BaseModel Class .....')
        self.base = BaseModel()
        self.id = self.base.id
        self.created_at = self.base.created_at
        self.updated_at = self.base.updated_at

    def tearDown(self):
        """ remove test instances """
        del self.base
        print(".................................\n\n")
        print("..... End Test BaseModel Class .....\n\n")
        print(".................................\n\n")

    def test_instance(self):
        """ Test if instance of BaseModel """
        print('... Testing instance of BaseModel ...')
        self.assertIsInstance(self.base, BaseModel)

    def test_id_type(self):
        """ Test if id type str """
        print('... Testing if id type of str ...')
        self.assertIsInstance(self.base.id, str)

    def test_created_at_type(self):
        """ Test created_at type  """
        print('... Testing if created_at is datetime type ...')
        self.assertIsInstance(self.base.created_at, datetime)

    def test_correct_created_at(self):
        """ Test correct created_at of BaseModel"""
        print('... Test for correct created_at ...')
        self.assertEqual(self.created_at, self.base.created_at)

    def test_updated_at(self):
        """ Test updated_at of BaseModel"""
        print('... Test updated_at of BaseModel ...')
        self.assertIsInstance(self.base.updated_at, datetime)

    def test_to_dict(self):
        """ Test to_dict method """
        print('... Testing to_dict method of BaseModel ...')
        base_dict = self.base.to_dict()
        self.assertIsInstance(base_dict, dict)
        self.assertEqual(base_dict['__class__'], 'BaseModel')
        self.assertEqual(base_dict['id'], self.id)
        self.assertEqual(base_dict['created_at'], self.created_at.isoformat())
        self.assertEqual(base_dict['updated_at'], self.updated_at.isoformat())

if __name__=="__main__":
    unittest.main()

