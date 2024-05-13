"""DB module
"""
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound # moved to sqlalchemy.exec in the v 1.4.x
from sqlalchemy.exc import InvalidRequestError
from .account import Base, Account
from .session import SessionAuth
from os import getenv
import models
from models import (
    Employee, Company, Department,
    Job, Form, Field, storage
)



def create_sqlite_connection(db_path):
    return sqlite3.connect(db_path)

env = getenv('HRPRO_ENV')
mysql_user = getenv('HRPR_MYSQL_USER')
mysql_pwd = getenv('HRPRO_MYSQL_PWD')
mysql_host = getenv('HRPRO_MYSQL_HOST')
mysql_db = getenv('HRPRO_ACCOUNTS_DB_NAME')


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".\
                                     format(mysql_user, mysql_pwd,
                                            mysql_host, mysql_db),
                                     echo=False)
        if env == 'test':
            Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def close(self) -> None:
        """Close the session
        """
        if self.__session is not None:
            self.__session.remove()
            self.__session = None
    
    def add_account(self, account_info: dict, company_info: dict) -> Account:
        """Add a new account to the database
        """
        try:
            employee_info = {
                "first name": account_info.get("first_name"),
                "last name": account_info.get("last_name"),
                "email": account_info.get("email"),
                "role": account_info.get("role"),
            }
            if account_info['role'] == 'admin':
                company = self.add_company(company_info)
                company.save()
            else:
                employee_id = company_info.get("employee_id", None)
                if not employee_id:
                    raise ValueError("Request error")
                company = storage.get_company_by_employee_id(employee_id)
                if not company:
                    raise InvalidRequestError("Company not found")
            new_employee = self.add_employee(employee_info)
            new_account = Account(**account_info, employee_id=new_employee.id)
            company.employees.append(new_employee)
            if account_info['role'] == 'admin':
                company.departments.append(new_employee.department)
                company.jobs.append(new_employee.job)
            company.save()
            self._session.add(new_account)
            self._session.commit()
        except Exception as err:
            self._session.rollback()
            new_account = None
            raise ValueError("Error creating account: {}".format(err))
        return new_account
    
    def add_company(self, company_info: dict) -> Company:
        """Creates new company
        Args:
            company_info: company information
        Returns:
            created company
        """
        new_company = Company(**company_info)
        new_company.save()
        emp_form = Form(name="employee", description="employee form")
        dep_form = Form(name="department", description="department form")
        job_form = Form(name="job", description="job form")
        emp_form.fields.append(Field(name="first name", type="text", is_required=False, position=1))
        emp_form.fields.append(Field(name="last name", type="text", is_required=False, position=2))
        emp_form.fields.append(Field(name="email", type="email", is_required=True, position=3))
        dep_form.fields.append(Field(name="name", type="text", is_required=True, position=1))
        job_form.fields.append(Field(name="title", type="text", is_required=True, position=1))
        for form in [emp_form, dep_form, job_form]:
            new_company.forms.append(form)
        new_company.save()
        return new_company
    
    def add_employee(self, employee_info: dict) -> Employee:
        """Creates new Emplyee
        Args:
            employee_info: employee information
        Returns:
            created employee
        """
        if "role" not in employee_info:
            raise ValueError("employee role is not defined")
        if employee_info["role"] in ["hr", "employee"]:
            try:
                emp_department = storage.find_department_by(name=employee_info["department"])
                emp_job = storage.find_job_by(title=employee_info["job title"])
            except:
                raise ValueError("Employee department or job not found")
        else:
            emp_department = Department(name="hr", info='{"name": "hr"}')
            emp_job = Job(title="hr", info='{"title": "hr"}')
        employee_info = str(employee_info)
        new_employee = Employee(info=employee_info)
        new_employee.department = emp_department
        new_employee.job = emp_job
        new_employee.save()
        return new_employee
    
    def find_account_by(self, **kwargs) -> Account:
        """Finds a account based on a set of filters.
        """
        for key in kwargs.keys():
            if not hasattr(Account, key):
                raise InvalidRequestError()
        account =  self._session.query(Account).filter_by(**kwargs).first()
        if account:
            return account
        else:
            raise NoResultFound()

    def get_session(self, session_id: str) -> SessionAuth:
        """Get a session by its id
        """
        return self._session.query(SessionAuth).\
            filter(SessionAuth.id == session_id).first()
        
    def delete_session(self, session_id: str) -> None:
        """Delete a session
        """
        session = self.get_session(session_id)
        if session is not None:
            self._session.delete(session)
            self._session.commit()
        else:
            raise NoResultFound("Session not found")

    def find_account_by_session_id(self, session_id: str) -> Account:
        """Find an account by session id
        """
        session = self.get_session(session_id)
        if session:
            return session.account
        else:
            return None
    
    def update_account(self, account_id: int, **kwargs) -> None:
        """Update a account in the database
        """
        account = self._session.query(Account).filter(Account.id == account_id).first()
        if account is not None:
            for key, value in kwargs.items():
                if hasattr(Account, key):
                    setattr(Account, key, value)
                else:
                    raise ValueError()
            self._session.commit()
