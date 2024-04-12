#!/usr/bin/env python3

from models.base_model import BaseModel, Base
from models.employee import Employee
from models.company import Company
from models.department import Department
from models.form import Form
from models.job import Job
from models.field import Field
from os import getenv


if __name__ not in ['file_storage', 'db_storage']:
    if getenv('HRPRO_TYPE_STORAGE') == 'db':
        from models.engine.db_storage import DBStorage
        storage = DBStorage()
    else:
        from models.engine.file_storage import FileStorage
        storage = FileStorage()

    storage.reload()
