#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from os import getenv


class Employee(BaseModel, Base):
    """Employee class"""
    __tablename__ = 'employees'

    company_id = Column(String(50),
                        ForeignKey('companies.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    job_id = Column(String(50),
                        ForeignKey('jobs.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    department_id = Column(String(50),
                        ForeignKey('departments.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    info = Column(Text, nullable=True)
    
    if getenv('HRPRO_TYPE_STORAGE') == 'db':
        department = relationship("Department", back_populates="employees")
        job = relationship("Job", back_populates="employees")
        company = relationship("Company", back_populates="employees")
        attendances = relationship("Attendance", back_populates="employee",
                                   cascade="all, delete-orphan")
        absences = relationship("Absence", back_populates="employee",
                                cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
