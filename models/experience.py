#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import (
    Column, String, Text,
    Date, ForeignKey,
    )
from sqlalchemy.orm import relationship


class Experience(BaseModel, Base):

    __tablename__ = 'experiences'

    employee_id = Column(String(50),
                        ForeignKey('employees.id', ondelete='CASCADE',
                                    onupdate='CASCADE'),
                        nullable=False
                        )
    company = Column(String(50), nullable=False)
    job_title = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)

    employee = relationship("Employee", back_populates="experiences")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["employee"] = "{} {}".format(self.employee.first_name,
                                                self.employee.last_name)
        new_dict["employee_uri"] = "http://localhost:5000/api/v1/employees/{}".\
            format(self.employee_id)
        new_dict["uri"] = "http://localhost:5000/api/v1/experiences/{}".\
            format(self.id)
        return new_dict