#!/usr/bin/python3
""" This module defines a class called DBStorage that represents the
database storage engine for the AirBnB clone project.
"""

from models import *
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar, Union


classes_dict = {
    "Company": Company, "Department": Department,
    "Job": Job, "Employee": Employee, "Form": Form,
    "Field": Field,
}

class DBStorage:
    __engine = None
    __session = None

    @property
    def _session(self) -> TypeVar['Session']:
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

    def all(self, cls: str = None) -> dict:
        """Returns the dictionary __objects"""

        if not isinstance(cls, str):
            raise TypeError("Expected a string for cls parameter")

        if cls and cls in classes_dict:
            cls = classes_dict[cls]
            query_list = self.__session.query(cls).all()
        else:
            query_list = []
            for cls in classes_dict.values():
                query_list.extend(self.__session.query(cls).all())
        obj = {type(obj).__name__ + '.' + obj.id: obj for obj in query_list}
        return obj

    def new(self, obj: TypeVar['BaseModel']) -> None:
        """This method adds the specified object to the current database
        session
        """
        self.__session.add(obj)

    def save(self) -> None:
        """This method commits all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj: TypeVar['BaseModel'] = None) -> None:
        """This method deletes the specified object from the current database
        session"""
        if obj:
            self.__session.delete(obj)

    def reload(self) -> None:
        """This method creates all tables in the database and initializes a
        new session with the current database engine
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self) -> None:
        """This method calls remove() on the private session attribute
        (self.__session) or close() on the class Session"""
        self.__session.remove()

    def get(self, cls: str, id: str) -> Union[TypeVar['BaseModel'], None]:
        """This method retrieves one object based on the class name and its ID
        """

        if not isinstance(cls, str):
            raise TypeError("Expected a string for cls parameter")

        if cls and cls in classes_dict:
            cls = classes_dict[cls]
            return self.__session.query(cls).filter(cls.id == id).first()
        return None
    
    def get_company_by_name(self, name: str) -> Union[TypeVar['Company'], None]:
        """This method retrieves one company based on its name
        """
        return self.__session.query(Company).filter(Company.name == name).first()
    
    def get_company_by_employee_id(self, employee_id: str) -> Union[TypeVar['Company'], None]:
        """This method retrieves one company based on an employee's ID
        Args:
            employee_id:
        Returns:
            company
        """
        employee = self.get(Employee, employee_id)
        return employee.company if employee else None
    
    def find_form_by_(self, **kwargs) -> Union[TypeVar['Form'], None]:
        """Finds a account based on a set of filters.
        """
        if not kwargs:
            raise InvalidRequestError("No filter criteria")
        for key in kwargs.keys():
            if not hasattr(Form, key):
                raise InvalidRequestError("Invalid filter key")
        form = self.__session.query(Form).filter_by(**kwargs).first()
        return form
        
    def find_job_by(self, **kwargs) -> Union[TypeVar['Job'], None]:
        """Finds a job based on a set of filters.
        """
        if not kwargs:
            raise InvalidRequestError("No filter criteria")
        for key in kwargs.keys():
            if not hasattr(Job, key):
                raise InvalidRequestError("Invalid filter key")
        job = self.__session.query(Job).filter_by(**kwargs).first()
        return job
        
    def find_department_by(self, **kwargs) -> Union[TypeVar['Department'], None]:
        """Finds department based on a set of filters
        """
        if not kwargs:
            raise InvalidRequestError("No filter criteria")
        for key in kwargs.keys():
            if not hasattr(Department, key):
                raise InvalidRequestError("Invalid filter key")
        department = self.__session.query(Department).filter_by(**kwargs).first()
        return department
        
    def find_employee_by(self, **kwargs) -> Union[TypeVar['Employee'], None]:
        """Finds employee based on a set of filters
        """
        if not kwargs:
            raise InvalidRequestError("No filter criteria")
        for key in kwargs.keys():
            if not hasattr(Employee, key):
                raise InvalidRequestError("Invalid filter key")
        employee = self.__session.query(Employee).filter_by(**kwargs).first()
        return employee
