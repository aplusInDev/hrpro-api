#!/usr/bin/env python3

""" training evaluation """
from models import BaseModel, Base
from sqlalchemy import (
    Column, String, ForeignKey,
    Text, Integer, Boolean
    )
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint


class Evaluation(BaseModel, Base):
    """Evaluation class"""
    __tablename__ = 'evaluations'
    training_id = Column(
        String(50),
        ForeignKey('trainings.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )
    employee_id = Column(
        String(50),
        ForeignKey('employees.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )
    score = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=True)
    anonimous = Column(Boolean, nullable=False, default=0)
    __table_args__ = (UniqueConstraint('training_id', 'employee_id', name='_training_employee_uc'),)
    training = relationship("Training", back_populates="evaluations")
    employee = relationship("Employee", back_populates="evaluations")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        if self.anonimous:
            trainee_name = "Anonimous"
        else:
            trainee_name = self.employee.first_name +\
                " " + self.employee.last_name
        new_dict = super().to_dict().copy()
        new_dict["training"] = "http://localhost:5000/api/v1/trainings/{}".\
            format(self.training_id)
        new_dict["employee"] = trainee_name
        del new_dict["employee_id"]
        new_dict["uri"] = "http://localhost:5000/api/v1/trainings/{}".\
            format(self.id)
        return new_dict
