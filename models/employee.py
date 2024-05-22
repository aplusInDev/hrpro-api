#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import (
    Column, String, Date,
    ForeignKey, Text, Integer,
    )
from sqlalchemy.orm import relationship
from datetime import date


class Employee(BaseModel, Base):
    """Employee class"""
    __tablename__ = 'employees'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    leave_balance = Column(Integer, nullable=True, default=0)
    hire_date = Column(Date, nullable=True)
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
    position_info = Column(Text, nullable=True)

    department = relationship("Department", back_populates="employees")
    job = relationship("Job", back_populates="employees")
    company = relationship("Company", back_populates="employees")
    attendances = relationship("Attendance", back_populates="employee",
                                cascade="all, delete-orphan")
    absences = relationship("Absence", back_populates="employee",
                            cascade="all, delete-orphan")
    leaves = relationship("Leave", back_populates="employee",
                          cascade="all, delete-orphan")
    trainings = relationship("Training", secondary="training_trainees",
                            back_populates="trainees")
    evaluations = relationship("Evaluation", back_populates="employee",
                                cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="employee",
                                cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="employee",
                               cascade="all, delete-orphan")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "hire_date" not in kwargs:
            self.hire_date = date.today()

    def to_dict(self):
        new_dict = super().to_dict().copy()
        return new_dict

