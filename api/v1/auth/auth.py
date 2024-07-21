#!/usr/bin/env python3

from .auth_db import DB
from .account import Account
from .session import SessionAuth
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from flask import render_template
from flask_mail import Message
from os import getenv
from models import storage, Employee, Job, Department
import string
import secrets


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def close(self):
        """Close the database connection
        """
        self._db.close()

    def send_activation_mail(self, company_id: str, email: str, name: str) -> None:
        """Send activation mail to registred user
        """
        from api.v1.app import mail
        try:
            account = self._db.find_account_by(
                email=email,
                company_id=company_id
            )
            activation_session = SessionAuth(session_duration=420)
            account.sessions.append(activation_session)
            account.tmp_token = activation_session.id
            self._db._session.commit()
            data = {
                "name": name,
                "activation_link": "http://localhost:5000/api/v1/activate?" +
                "email={}&company_id={}&activation_token={}".\
                    format(email, company_id, account.tmp_token)
                }
            msg = Message("Activation email", sender=getenv('HRPRO_EMAIL'),
                        recipients=[account.email])
            msg.html = render_template("email_activation.html", data=data)
            mail.send(msg)
        except NoResultFound:
            raise ValueError("Faild to send activation email")
        except Exception as err:
            raise ValueError(str(err))
        
    def send_welcome_mail(self, name:str, email: str, password: str) -> None:
        """Send welcome mail to new employee
        """
        from api.v1.app import mail
        data = {
            "name": name,
            "email": email,
            "password": password,
            "login_link": "http://localhost:3000/login"
        }
        msg = Message("Welcome to HRPro", sender=getenv('HRPRO_EMAIL'),
                    recipients=[email])
        msg.html = render_template("email_welcome.html", data=data)
        try:
            mail.send(msg)
        except Exception as err:
            raise ValueError(str(err))

    def register_admin(self, admin_info: dict, company_info: dict):
        """ register admin """
        if storage.get_company_by_name(company_info.get("name")):
            raise ValueError("Giving company name already exists")
        new_company = self._db.add_company(company_info)
        if new_company is None:
            raise Exception("faild to create new compnay")
        hashed_password = _hash_password(admin_info["password"])
        admin_info["hashed_password"] = hashed_password
        employee_details = {
            "first_name": admin_info["first_name"],
            "last_name": admin_info["last_name"],
            "email": admin_info["email"],
        }
        try:
            admin_department = Department(
                name="hr",
                company_id=new_company.id,
                info="{'name': 'hr'}"
            )
            admin_department.save()
            admin_job = Job(
                title="hr",
                company_id=new_company.id,
                info="{'title': 'hr'}"
            )
            admin_job.save()
            new_admin = Employee(
                **admin_info,
                info=employee_details,
                company_id=new_company.id,
                job_id=admin_job.id,
                department_id=admin_department.id
            )
            new_admin.company = new_company
            new_admin.save()
        except Exception:
            new_company.delete()
            raise Exception("faild to create new admin")
        try:
            new_admin_account = Account(
                **admin_info,
                role="admin",
                employee_id=new_admin.id,
                company_id=new_company.id
            )
            new_admin_account.save()
            return new_admin_account
        except Exception:
            new_admin.delete()
            new_company.delete()
            raise Exception("faild to create admin account")

    def register_employee(self, employee_info: dict):
        """ register new employee """
        company_id = employee_info.get("company_id")
        company = storage.get("Company", company_id)
        if not company:
            raise ValueError("Company not found")
        email = employee_info["email"]
        if self._db.find_account_by(email=email, company_id=company_id):
            raise Exception("faild to register the new employee," +
                            "please try again.")
        employee_details = {
            "first_name": employee_info["first_name"],
            "last_name": employee_info["last_name"],
            "email": employee_info["email"],
        }
        try:
            new_employee = Employee(
                **employee_info,
                info=employee_details
            )
            new_employee.company = company
            new_employee.save()
        except Exception:
            raise Exception("faild to create new employee")
        password = _generate_random_pass()
        hashed_password = _hash_password(password)
        employee_info["hashed_password"] = hashed_password
        try:
            new_account = Account(
                **employee_info,
                role=employee_info.get("role"),
                employee_id=new_employee.id,
                company_id=company_id
            )
            new_account.save()
        except Exception:
            new_employee.delete()
            raise Exception("faild to create employee account")
    
    def activate_account(self, account_id: str, activation_token: str) -> bool:
        """Activate the account
        """
        session = self._db.get_session(activation_token)
        if not session:
            raise ValueError("token not valid")
        try:
            account = self._db.find_account_by(
                id=account_id,
                tmp_token=activation_token
            )
        except NoResultFound:
            self._db.delete_session(activation_token)
            raise ValueError("No account with this token found")
        # check if session expired
        # if datetime.now() - session.created_at > timedelta(minutes=session.session_duration):
        #     account.tmp_token = None
        #     self._db.delete_session(activation_token)
        #     raise ValueError("Session token expired, another email sent {}".format(datetime.now()))
        if session and account.tmp_token == activation_token:
            account.is_active = True
            account.tmp_token = None
            self._db.delete_session(activation_token)
            return True
    
    def valid_login(self, company_id: str, email: str, password: str) -> bool:
        """Check if the login is valid.
        """
        try:
            account = self._db.find_account_by(
                email=email,
                company_id=company_id
            )
            return bcrypt.checkpw(
                password.encode(),
                account.hashed_password.encode()
            )
        except NoResultFound:
            return False
        
    def create_session(self,company_id: str, email: str) -> str:
        """Create a new session
        """
        try:
            account = self._db.find_account_by(
                email=email,
                company_id=company_id
            )
            new_session = SessionAuth()
            account.sessions.append(new_session)
            self._db.new(new_session)
            self._db.save()
            return new_session.id
        except NoResultFound:
            return None
        
    def get_current_user(self, company_id: str, email: str) -> dict:
        """Retrive current user
        """
        try:
            account = self._db.find_account_by(
                email=email,
                company_id=company_id
            )
            current_user = {
                "employee_id": account.employee_id,
                "email": account.email,
                "role": account.role,
                "company_id": account.company_id,
            }
            return current_user
        except NoResultFound:
            return None
        
    def get_account_from_session_id(self, session_id: str):
        """Get the account from the session id
        """
        session = self._db.get_session(session_id)
        if session is None:
            raise NoResultFound("Session not found")
        return session.account
        
    def destroy_session(self, session_id: str) -> bool:
        """Destroy the session
        """
        try:
            self._db.delete_session(session_id=session_id)
            return True
        except NoResultFound:
            return False
        
    def get_reset_password_token(self, company_id: str, email: str) -> str:
        """Get the reset password token
        """
        try:
            account = self._db.find_account_by(
                email=email,
                company_id=company_id
            )
            tmp_session = SessionAuth(session_duration=200)
            account.sessions.append(tmp_session)
            account.tmp_token = tmp_session.id
            tmp_session.save()
            return account.tmp_token
        except NoResultFound:
            raise ValueError("Account not found")
        
    def update_password(self, login_details: dict) -> None:
        """Update the password
        """
        company_id = login_details["company_id"]
        email = login_details["email"]
        password = login_details["password"]
        new_password = login_details["new_password"]
        if not self.valid_login(company_id, email, password):
            raise ValueError("Invalid login")
        if self.valid_login(company_id, email, new_password):
            raise ValueError(
                "New password cannot be the same as the old password"
            )
        try:
            account = self._db.find_account_by(
                email=email,
                company_id=company_id
            )
            account.hashed_password = _hash_password(new_password)
            # account.save()
            self._db.save()
        except NoResultFound:
            raise NoResultFound("Account not found")

def _hash_password(password: str) -> str:
    """Hash password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def _generate_random_pass():
    """Generate random password for new employee
    """
    symbols = ['*', '@', '_']
    password = ""

    for _ in range(2):
        password += secrets.choice(string.ascii_lowercase)
        password += secrets.choice(string.ascii_uppercase)
        password += secrets.choice(string.digits)
        password += secrets.choice(symbols)
    
    return password
