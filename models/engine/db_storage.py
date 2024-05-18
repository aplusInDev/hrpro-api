#!/usr/bin/python3
""" This module defines a class called DBStorage that represents the
database storage engine for the AirBnB clone project.
"""

from models import *
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


classes_list = [Company, Department, Job, Employee, Form, Field]

class DBStorage:
    __engine = None
    __session = None

    @property
    def _session(self):
        """This method creates a new session with the current database engine
        """
        if self.__session is None:
            Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
            self.__session = scoped_session(Session)
        return self.__session

    def __init__(self):
        """This method initializes a new instance of the DBStorage class"""
        env = getenv('HRPRO_ENV')
        mysql_user = getenv('HRPR_MYSQL_USER')
        mysql_pwd = getenv('HRPRO_MYSQL_PWD')
        mysql_host = getenv('HRPRO_MYSQL_HOST')
        mysql_db = getenv('HRPRO_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(mysql_user, mysql_pwd,
                                             mysql_host, mysql_db),
                                      pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns the dictionary __objects"""

        if cls and cls in classes_list:
            query_list = self.__session.query(cls).all()
        else:
            query_list = []
            for cls in classes_list:
                query_list.extend(self.__session.query(cls).all())
        obj = {type(obj).__name__ + '.' + obj.id: obj for obj in query_list}
        return obj

    def new(self, obj):
        """This method adds the specified object to the current database
        session
        """
        self.__session.add(obj)

    def save(self):
        """This method commits all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """This method deletes the specified object from the current database
        session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """This method creates all tables in the database and initializes a
        new session with the current database engine
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """This method calls remove() on the private session attribute
        (self.__session) or close() on the class Session"""
        self.__session.remove()

    def get(self, cls, id):
        """This method retrieves one object based on the class name and its ID
        """
        if cls and cls in classes_list:
            return self.__session.query(cls).filter(cls.id == id).first()
        return None
    
    def get_company_by_name(self, name: str):
        """This method retrieves one company based on its name
        """
        return self.__session.query(Company).filter(Company.name == name).first()
    
    def get_company_by_employee_id(self, employee_id: str) -> Company:
        """This method retrieves one company based on an employee's ID
        Args:
            employee_id:
        Returns:
            company
        """
        employee = self.get(Employee, employee_id)
        return employee.company if employee else None
    
    def get_emplyee_info(self, employee_id: str) -> dict:
        """This method retrieves employee info based on its ID
        """
        employee = self.get(Employee, employee_id)
        return eval(employee.info) if employee else None
    
    def find_form_by_(self, **kwargs) -> Form:
        """Finds a account based on a set of filters.
        """
        for key in kwargs.keys():
            if not hasattr(Form, key):
                raise InvalidRequestError("Invalid filter key")
        form = self.__session.query(Form).filter_by(**kwargs).first()
        if form:
            return form
        else:
            raise NoResultFound("form not found")
        
    def find_job_by(self, **kwargs) -> Job:
        """Finds a job based on a set of filters.
        """
        for key in kwargs.keys():
            if not hasattr(Job, key):
                raise InvalidRequestError("Invalid filter key")
        job = self.__session.query(Job).filter_by(**kwargs).first()
        if job:
            return job
        else:
            raise NoResultFound("job not found")
        
    def find_department_by(self, **kwargs) -> Department:
        """Finds department based on a set of filters
        """
        for key in kwargs.keys():
            if not hasattr(Department, key):
                raise InvalidRequestError("Invalid filter key")
        department = self.__session.query(Department).filter_by(**kwargs).first()
        if department:
            return department
        else:
            raise NoResultFound("department not found")
        
    def find_employee_by(self, **kwargs):
        """Finds employee based on a set of filters
        """
        for key in kwargs.keys():
            if not hasattr(Employee, key):
                raise InvalidRequestError("Invalid filter key")
        employee = self.__session.query(Employee).filter_by(**kwargs).first()
        if employee:
            return employee
        else:
            raise NoResultFound("employee not found")
