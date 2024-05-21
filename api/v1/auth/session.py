#!/usr/bin/env python3

""" Session management
"""

from .account import Base
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship


class SessionAuth(Base):
    """Session class
    """
    __tablename__ = 'sessions'
    id = Column(String(128), primary_key=True, default=lambda: str(uuid4()))
    account_id = Column(String(128), ForeignKey(
        'accounts.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    session_duration = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now())

    account = relationship("Account", back_populates="sessions")

    def __init__(self, *args, **kwargs):
        """Session constructor
        """
        if kwargs:
            if "id" not in kwargs:
                self.id = str(uuid4())
            for key, value in kwargs.items():
                setattr(self, key, value)

