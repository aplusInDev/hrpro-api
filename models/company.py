#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship


class Company(BaseModel, Base):
    """Company class"""
    __tablename__ = 'companies'
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=True, unique=True)
    phone = Column(String(50), nullable=True, unique=True)
    website = Column(String(50), nullable=True, unique=True)

    departments = relationship("Department", back_populates="company",
                                cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="company",
                                cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="company",
                        cascade="all, delete-orphan")
    forms = relationship("Form", back_populates="company",
                            cascade="all, delete-orphan")
    trainings = relationship("Training", back_populates="company",
                            cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes a new instance"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["departments"] = {
            department.name: "http://localhost:5000/api/v1/departments/" +
            department.id for department in self.departments
            }
        new_dict["employees"] = {
            employee.first_name + " " + employee.last_name:
            "http://localhost:5000/api/v1/employees/" + employee.id
            for employee in self.employees
            }
        new_dict["jobs"] = {
            job.title: "http://localhost:5000/api/v1/jobs/" + job.id
            for job in self.jobs
            }
        new_dict["forms"] = {
            form.name: "http://localhost:5000/api/v1/forms/" + form.id
            for form in self.forms
            }
        new_dict["trainings"] = {
            training.title: "http://localhost:5000/api/v1/trainings/" + training.id
            for training in self.trainings
        }
        new_dict["uri"] = "http://localhost:5000/api/v1/companies/" + self.id
        return new_dict
