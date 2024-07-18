#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import (
    Column, String, Date, ForeignKey
    )
from sqlalchemy.orm import relationship


class Certificate(BaseModel, Base):
    """ training certificate """

    __tablename__ = 'certificates'
    employee_id = Column(
        String(50),
        ForeignKey('employees.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )
    institution = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)

    employee = relationship("Employee", back_populates="certificates")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["employee"] = "{} {}".format(self.employee.first_name,
                                                self.employee.last_name)
        new_dict["employee_uri"] = "http://localhost:5000/api/v1/employees/{}".\
            format(self.employee_id)
        return new_dict
