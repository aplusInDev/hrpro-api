#!/usr/bin/env python3

from models import BaseModel, Base
# from models import Employee
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class Company(BaseModel, Base):
    """Company class"""
    __tablename__ = 'companies'


    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(50), nullable=True)

    departments = relationship("Department", back_populates="company",
                                cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="company",
                                cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="company",
                        cascade="all, delete-orphan")
    forms = relationship("Form", back_populates="company",
                            cascade="all, delete-orphan")

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["departments"] = [department.to_dict() for department in self.departments]
        new_dict["employees"] = [employee.to_dict() for employee in self.employees]
        new_dict["jobs"] = [job.to_dict() for job in self.jobs]
        new_dict["forms"] = [form.to_dict() for form in self.forms]
        return new_dict

    def __init__(self, *args, **kwargs):
        """Initializes a new instance"""
        super().__init__(*args, **kwargs)
