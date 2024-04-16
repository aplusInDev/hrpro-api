#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from os import getenv


class Attendance(BaseModel, Base):
    """Attendance class"""
    __tablename__ = 'attendances'

    employee_id = Column(String(50),
                         ForeignKey('employees.id', ondelete='CASCADE',
                                    onupdate='CASCADE'),
                         nullable=False
                         )
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)

    if getenv('HRPRO_TYPE_STORAGE') == 'db':
        employee = relationship("Employee", back_populates="attendances")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
