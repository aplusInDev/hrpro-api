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
    
    def add_account(self, email: str, hashed_password: str, role: str) -> Account:
        """Add a new account to the database
        """
        try:
            new_account = Account(email=email, hashed_password=hashed_password, role=role)
            self._session.add(new_account)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_account = None
        return new_account
    
    def find_account_by(self, **kwargs) -> Account:
        """Finds a account based on a set of filters.
        """
        for key, value in kwargs.items():
            if hasattr(Account, key):
                result = self._session.query(Account).\
                    filter(getattr(Account, key) == value).\
                    first()
                if result is not None:
                    return result
            else:
                raise InvalidRequestError()
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
