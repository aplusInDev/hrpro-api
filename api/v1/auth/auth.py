#!/usr/bin/env python3

#!/usr/bin/env python3


from .db import DB
from .account import Account
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def close(self):
        """Close the database connection
        """
        self._db.close()

    def register_account(self, email: str, password: str, role: str ="standard") -> Account:
        """Register a new account.
        """
        if self._db._session.query(Account).filter(Account.email == email).first():
            raise ValueError("Account <{}> already exists".format(email))
        hashed_password = _hash_password(password)
        return self._db.add_account(email, hashed_password, role)
    
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
            account.session_id = _generate_uuid()
            self._db._session.commit()
            return account.session_id
        except NoResultFound:
            return None
        
    def get_account_from_session_id(self, session_id: str) -> Account:
        """Get the account from the session id
        """
        try:
            return self._db.find_account_by(session_id=session_id)
        except NoResultFound:
            return None
        
    def destroy_session(self, session_id: str) -> bool:
        """Destroy the session
        """
        try:
            account = self._db.find_account_by(session_id=session_id)
            account.session_id = None
            self._db._session.commit()
            return True
        except NoResultFound:
            return False
        
    def get_reset_password_token(self, email: str) -> str:
        """Get the reset password token
        """
        try:
            account = self._db.find_account_by(email=email)
            account.reset_token = _generate_uuid()
            self._db._session.commit()
            return account.reset_token
        except NoResultFound:
            raise ValueError
        
    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password
        """
        try:
            account = self._db.find_account_by(reset_token=reset_token)
            account.hashed_password = _hash_password(password)
            account.reset_token = None
            self._db._session.commit()
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> str:
    """Hash password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def _generate_uuid() -> str:
    """Generate a new UUID
    """
    return str(uuid4())