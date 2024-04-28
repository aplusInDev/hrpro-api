#!/usr/bin/env python3

from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(String(128), primary_key=True)
    email = Column(String(128), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    role = Column(String(128), nullable=False, default="standard")
    session_id = Column(String(128), nullable=True)
    reset_token = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        if kwargs:
            if "id" not in kwargs:
                self.id = str(uuid4())
            for key, value in kwargs.items():
                setattr(self, key, value)
