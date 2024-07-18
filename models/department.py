#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint


class Department(BaseModel, Base):
    __tablename__ = 'departments'

    name = Column(String(50), nullable=False)
    company_id = Column(
        String(50),
        ForeignKey('companies.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )
    info = Column(Text, nullable=True)
    __table_args__ = (
        UniqueConstraint('name', 'company_id', name='unique_department'),
    )
    company = relationship("Company", back_populates="departments")
    employees = relationship("Employee", back_populates="department",
                                cascade="all, delete-orphan")
    trainings = relationship("Training", back_populates="department",
                            cascade="all, delete-orphan")
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["employees"] = {
            employee.first_name + " " + employee.last_name:
            "http://localhost:5000/api/v1/employees/" + employee.id
            for employee in self.employees
            }
        new_dict["company"] = "http://localhost:5000/api/v1/companies/{}".\
            format(self.company_id)
        new_dict["trainings"] = {
            training.title: "http://localhost:5000/api/v1/trainings/" + training.id
            for training in self.trainings
        }
        new_dict["info"] = eval(self.info) if self.info else {}
        new_dict["uri"] = "http://localhost:5000/api/v1/departments/" + self.id
        return new_dict
