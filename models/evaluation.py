#!/usr/bin/env python3

""" training evaluation """
from models import BaseModel, Base
from sqlalchemy import (
    Column, String, ForeignKey,
    Text, Integer, Boolean
    )
from sqlalchemy.orm import relationship


class Evaluation(BaseModel, Base):
    """Evaluation class"""
    __tablename__ = 'evaluations'

    training_id = Column(String(50),
                         ForeignKey('trainings.id', ondelete='CASCADE',
                                    onupdate='CASCADE'),
                         nullable=False
                         )
    employee_id = Column(String(50),
                         ForeignKey('employees.id', ondelete='CASCADE',
                                    onupdate='CASCADE'),
                         nullable=False
                         )
    score = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=True)
    anonimous = Column(Boolean, nullable=False, default=0)

    training = relationship("Training", back_populates="evaluations")
    employee = relationship("Employee", back_populates="evaluations")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["training"] = "http://localhost:5000/api/v1/trainings/{}".\
            format(self.training_id)
        new_dict["employee"] = "http://localhost:5000/api/v1/employees/{}".\
            format(self.employee_id)
        return new_dict
