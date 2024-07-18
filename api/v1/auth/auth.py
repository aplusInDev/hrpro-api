#!/usr/bin/env python3

from .auth_db import DB
from .account import Account
from .session import SessionAuth
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timedelta
from flask import render_template, jsonify
from flask_mail import Message
from os import getenv
from models import storage
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

    def send_activation_mail(self, email: str, name: str) -> None:
        """Send activation mail to registred user
        """
        from api.v1.app import mail
        try:
            account = self._db.find_account_by(email=email)
            activation_session = SessionAuth(session_duration=420)
            account.sessions.append(activation_session)
            account.tmp_token = activation_session.id
            self._db._session.commit()
            data = {
                "name": name,
                "activation_link": "http://localhost:5000/api/v1/activate?account_id={}&activation_token={}".\
                    format(account.id, account.tmp_token)
                }
            msg = Message("Activation email", sender=getenv('HRPRO_EMAIL'),
                        recipients=[account.email])
            msg.html = render_template("email_activation.html", data=data)
            try:
                mail.send(msg)
            except Exception as err:
                return jsonify({"sending email error:": str(err)}), 400
        except NoResultFound:
            return None
        
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
            return jsonify({"sending email error:": str(err)}), 400

    def register_admin(self, admin_info: dict, company_info: dict):
        """ register admin """
        try:
            self._db.find_account_by(email=admin_info.get("email"))
            raise ValueError("Account <{}> already exists".format(
                admin_info.get("email")))
        except NoResultFound:
            pass
        except Exception as err:
            raise err
        if storage.get_company_by_name(company_info.get("name")):
            raise ValueError("Giving company name already exists")
        hashed_password = _hash_password(admin_info.get("password"))
        admin_info["hashed_password"] = hashed_password
        if admin_info.get("password"):
            del admin_info["password"]
        return self._db.add_admin_account(admin_info, company_info)

    def add_employee_account(self, account_info: dict, position_info: dict):
        """ Add new employee account """
        company_id = position_info.get("company_id")
        del position_info["company_id"]
        company = storage.get("Company", company_id)
        if not company:
            raise ValueError("Company not found")
        account_info["hashed_password"] = _hash_password(account_info["password"])
        employee_info = account_info.copy()
        for key in ["password", "hased_password"]:
            if key in employee_info:
                del employee_info[key]
        role = employee_info.get("role")
        del employee_info["role"]
        try:
            new_employee = self._db.add_employee(role, employee_info, position_info)
        except ValueError as err:
            raise ValueError(str(err))
        new_employee.company = company
        new_employee.save()
        new_account = Account(**account_info, employee_id=new_employee.id)
        # self._db._session.add(new_account)
        # self._db._session.commit()
        new_account.save()
        return new_account
    
    def activate_account(self, account_id: str, activation_token: str) -> bool:
        """Activate the account
        """
        session = self._db.get_session(activation_token)
        if not session:
            raise ValueError("token not valid")
        try:
            account = self._db.find_account_by(id=account_id,
                                                tmp_token=activation_token)
        except NoResultFound:
            # self._db.delete_session(activation_token)
            session.delete()
            raise ValueError("No account with this token found")
        # check if session expired
        if datetime.now() - session.created_at > timedelta(minutes=session.session_duration):
            # self._db.delete_session(activation_token)
            session.delete()
            account.tmp_token = None
            self.send_activation_mail(account.email, account.first_name)
            raise ValueError("Session token expired, another email sent {}".format(datetime.now()))
        if session and account.tmp_token == activation_token:
            account.is_active = True
            account.tmp_token = None
            # self._db.delete_session(activation_token)
            # self._db._session.commit()
            session.delete()
            return True
    
    def valid_login(self, email: str, password: str) -> bool:
        """Check if the login is valid.
        """
        try:
            account = self._db.find_account_by(email=email)
            # if account.role == "admin" and not account.is_active:
            #     raise ValueError("account unactivated!")
            return bcrypt.checkpw(password.encode(), account.hashed_password.encode())
        except NoResultFound:
            return False
        
    def create_session(self, email: str) -> str:
        """Create a new session
        """
        try:
            account = self._db.find_account_by(email=email)
            account.sessions.append(SessionAuth())
            self._db._session.commit()
            return account.sessions[-1].id
        except NoResultFound:
            return None
        
    def get_current_user(self, email: str) -> dict:
        """Retrive current user
        """
        try:
            account = self._db.find_account_by(email=email)
            current_user = {
                "employee_id": account.employee.id,
                "email": account.email,
                "role": account.role,
                "company_id": account.employee.company_id,
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
        
    def get_reset_password_token(self, email: str) -> str:
        """Get the reset password token
        """
        try:
            account = self._db.find_account_by(email=email)
            tmp_session = SessionAuth(session_duration=20)
            account.sessions.append(tmp_session)
            account.tmp_token = tmp_session.id
            self._db._session.commit()
            return account.tmp_token
        except NoResultFound:
            raise ValueError("Account not found")
        
    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password
        """
        session = self._db.get_session(reset_token)
        if session:
            try:
                account = self._db.find_account_by(tmp_token=reset_token)
            except NoResultFound:
                self._db.delete_session(reset_token)
                raise ValueError("No account with this token found")
            # check if session expired
            if datetime.now() - session.created_at > timedelta(seconds=session.session_duration):
                self._db.delete_session(reset_token)
                account.tmp_token = None
                raise ValueError("Session token expired")
            account.hashed_password = _hash_password(password)
            self._db.delete_session(reset_token)
            account.tmp_token = None
            self._db._session.commit()
        else:
            raise ValueError("Session token not found")

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
