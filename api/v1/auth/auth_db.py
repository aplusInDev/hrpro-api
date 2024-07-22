#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound # moved to sqlalchemy.exec in the v 1.4.x
from sqlalchemy.exc import InvalidRequestError
from .account import Base, Account
from .session import SessionAuth
from os import getenv
from models import storage, Company



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
    
    def add_company(self, company_info: dict):
        """Creates new company
        Args:
            company_info: company information
        Returns:
            created company
        """
        try:
            new_company = Company(**company_info)
            new_company.save()
            return new_company
        except Exception:
            return None
    
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
    
    def update_account(self, account_id: str, **kwargs) -> None:
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
        
    def delete_account(self, account_id: str) -> str:
        """ Delete account """
        try:
            account = self.find_account_by(id=account_id)
            self._session.delete(account)
            self.save()
            return None
        except Exception as err:
            return str(err)

