#!/usr/bin/env python3

from uuid import uuid4
from sqlalchemy import Column, String, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models import storage
from sqlalchemy.schema import UniqueConstraint


Base = declarative_base()
role_enum = Enum("employee", "hr", "admin", name="role_type")


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(String(128), primary_key=True)
    email = Column(String(128), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    company_id = Column(String(128), nullable=False)
    employee_id = Column(String(128), nullable=False)
    role = Column(role_enum, nullable=False, default="employee")
    tmp_token = Column(String(128), nullable=True)
    is_active = Column(Boolean, nullable=False, default=False)
    __table_args__ = (UniqueConstraint('email', 'company_id', name='unique_email'),)
    sessions = relationship("SessionAuth", back_populates="account")

    def __init__(self, *args, **kwargs):
        if kwargs:
            if "id" not in kwargs:
                self.id = str(uuid4())
            for key, value in kwargs.items():
                setattr(self, key, value)

    @property
    def employee(self) -> None:
        return storage.get("Employee", self.employee_id)
    
    def save(self):
        """ save method """
        from . import db
        db.new(self)
        db.save()

    def delete(self) -> None:
        """ delete method """
        from . import db
        db.delete_account(self.id)
