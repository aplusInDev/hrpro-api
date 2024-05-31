#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class Job(BaseModel, Base):
    """Job class"""
    __tablename__ = 'jobs'

    title = Column(String(50), nullable=False)
    company_id = Column(String(50),
                        ForeignKey('companies.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    info = Column(Text, nullable=True)

    company = relationship("Company", back_populates="jobs")
    employees = relationship("Employee", back_populates="job",
                            cascade="all, delete-orphan")
    trainings = relationship("Training", back_populates="job",
                            cascade="all, delete-orphan")
    
    def __init__(self, *args, **kwargs):
        """Initializes a new instance"""
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
        new_dict["info"] = eval(self.info)
        new_dict["uri"] = "http://localhost:5000/api/v1/jobs/" + self.id
        return new_dict
