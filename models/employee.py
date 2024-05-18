#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from os import getenv


class Employee(BaseModel, Base):
    """Employee class"""
    __tablename__ = 'employees'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
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
        
        def to_dict(self):
            new_dict = super().to_dict().copy()
            new_dict["attendances"] = [attendance.to_dict() for attendance in self.attendances]
            new_dict["absences"] = [absence.to_dict() for absence in self.absences]
            return new_dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
