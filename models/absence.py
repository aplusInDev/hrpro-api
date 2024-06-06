#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Absence(BaseModel, Base):
    """Absence class"""
    __tablename__ = 'absences'

    employee_id = Column(String(50),
                         ForeignKey('employees.id', ondelete='CASCADE',
                                    onupdate='CASCADE'),
                         nullable=False
                         )
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    reason = Column(String(50), nullable=True)

    employee = relationship("Employee", back_populates="absences")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["employee"] = "http://localhost:5000/api/v1/employees/{}".\
            format(self.employee_id)
        new_dict["start_date"] = self.start_date.strftime('%Y-%m-%d')
        new_dict["end_date"] = self.end_date.strftime('%Y-%m-%d')
        new_dict["n_days"] = (self.end_date - self.start_date).days + 1
        return new_dict
