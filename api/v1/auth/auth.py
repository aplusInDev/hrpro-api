#!/usr/bin/env python3

#!/usr/bin/env python3


from .db import DB
from .account import Account
from .session import SessionAuth
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from datetime import datetime, timedelta
from flask import render_template, jsonify
from flask_mail import Message
from os import getenv


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def close(self):
        """Close the database connection
        """
        self._db.close()

    def send_activation_mail(self, email: str) -> None:
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
                "activation_link": "http://localhost:5000/api/v1/activate?account_id={}&activation_token={}".\
                    format(account.id, account.tmp_token)
                }
            # return data
            msg = Message("Activation email", sender=getenv('HRPRO_EMAIL'),
                        recipients=[account.email])
            msg.html = render_template("email_activation.html", data=data)
            try:
                mail.send(msg)
            except Exception as err:
                return jsonify({"sending email error:": str(err)}), 400
        except NoResultFound:
            return None

    def register_account(self, email: str, password: str, role: str ="standard") -> Account:
        """Register a new account.
        """
        if self._db._session.query(Account).filter(Account.email == email).first():
            raise ValueError("Account <{}> already exists".format(email))
        hashed_password = _hash_password(password)
        return self._db.add_account(email, hashed_password, role)
    
    def activate_account(self, account_id: str, activation_token: str) -> bool:
        """Activate the account
        """
        session = self._db.get_session(activation_token)
        if session:
            try:
                account = self._db.find_account_by(id=account_id,
                                                   tmp_token=activation_token)
            except NoResultFound:
                self._db.delete_session(activation_token)
                raise ValueError("No account with this token found")
            # check if session expired
            if datetime.now() - session.created_at > timedelta(seconds=session.session_duration):
                self._db.delete_session(activation_token)
                account.tmp_token = None
                raise ValueError("Session token expired")
            if session and account.tmp_token == activation_token:
                account.is_active = True
                account.tmp_token = None
                self._db.delete_session(activation_token)
                self._db._session.commit()
                return True
    
    def valid_login(self, email: str, password: str) -> bool:
        """Check if the login is valid.
        """
        try:
            account = self._db.find_account_by(email=email)
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
        
    def get_account_from_session_id(self, session_id: str) -> Account:
        """Get the account from the session id
        """
        try:
            return self._db.find_account_by_session_id(session_id=session_id)
        except NoResultFound:
            return None
        
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
