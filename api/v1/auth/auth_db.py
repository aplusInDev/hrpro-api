"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound # moved to sqlalchemy.exec in the v 1.4.x
from sqlalchemy.exc import InvalidRequestError
from .account import Base, Account
from .session import SessionAuth
from os import getenv
from models import (
    storage, Company, Department,
    Job, Form, Field, Employee,
)


env = getenv('HRPRO_ENV')
mysql_user = getenv('HRPRO_MYSQL_USER')
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
            self.recreate_tables(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    def recreate_tables(self, engine):
        """This method creates all tables in the database"""
        Base.metadata.create_all(engine)


    @property
    def _session(self):
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

    def reload(self) -> None:
        """ This method creates all tables in the database """
        Base.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def new(self, obj) -> None:
        """ This method adds the specified object to the database """
        self.__session.add(obj)

    def save(self) -> None:
        """ This method commits all changes in the database """
        self.__session.commit()

    def add_admin_account(self, account_info: dict, company_info: dict):
        """ Add new admin account """
        company = self.add_company(company_info)
        company.save()
        employee_info = account_info.copy()
        if employee_info.get("hashed_password"):
            del employee_info["hashed_password"]
        new_employee = self.add_employee("admin", employee_info)
        new_employee.company = company
        new_employee.save()
        company.jobs.append(new_employee.job)
        company.departments.append(new_employee.department)
        company.save()
        new_account = Account(**account_info, employee_id=new_employee.id,
                              role="admin")
        # self._session.add(new_account)
        # self.__session.commit()
        new_account.save()
        return new_account
    
    def add_company(self, company_info: dict):
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
    
    def add_employee(self, role: str, employee_info: dict,
                     position_info: dict={}):
        """Creates new Emplyee
        Args:
            employee_info: employee information
        Returns:
            created employee
        """
        if role in ["employee", "hr"]:
            try:
                employee_department = storage.find_department_by(name=position_info["department"])
            except:
                raise ValueError("Employee department not found")
            try:
                employee_job = storage.find_job_by(title=position_info["job_title"])
            except:
                raise ValueError("Employee job not found")
        elif role == "admin":
            employee_department = Department(name="hr", info='{"name": "hr"}')
            employee_job = Job(title="hr", info='{"title": "hr"}')
            position_info = {
                "department": "hr",
                "job_title": "hr",
            }
        else:
            raise ValueError("Invalid role")
        str_employee_info = str(employee_info)
        new_employee = Employee(**employee_info, info=str_employee_info)
        new_employee.department = employee_department
        new_employee.job = employee_job
        new_employee.save()
        return new_employee
    
    def find_account_by(self, **kwargs):
        """Finds a account based on a set of filters.
        """
        if not kwargs:
            return None
        for key in kwargs.keys():
            if not hasattr(Account, key):
                raise InvalidRequestError(f"Invalid filter criteria: {key}")
        account =  self._session.query(Account).filter_by(**kwargs).first()
        if not account:
            raise NoResultFound("account not found")
        return account

    def get_session(self, session_id: str):
        """Get a session by its id
        """
        return self._session.query(SessionAuth).\
            filter(SessionAuth.id == session_id).\
            first()
        
    def delete_session(self, session_id: str) -> None:
        """Delete a session
        """
        session = self.get_session(session_id)
        if session is not None:
            self._session.delete(session)
            self._session.commit()
        else:
            raise NoResultFound("Session not found")
    
    def update_account(self, account_id: int, **kwargs) -> None:
        """Update a account in the database
        """
        try:
            account = self.find_account_by(id=account_id)
            for key, value in kwargs.items():
                setattr(account, key, value)
            self._session.commit()
        except Exception as err:
            self._session.rollback()
            raise ValueError("Error updating account: {}".format(err))
