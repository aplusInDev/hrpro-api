#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text, Enum, Date
from sqlalchemy.orm import relationship
from datetime import datetime


leave_status = Enum("pending", "approved", "rejected", name="leave_status")


class Leave(BaseModel, Base):
    __tablename__= "leaves"

    employee_id = Column(String(50),
                        ForeignKey('employees.id', ondelete='CASCADE',
                                    onupdate='CASCADE'),
                        nullable=False
                        )
    leave_type = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(leave_status, nullable=False, default="pending")

    employee = relationship("Employee", back_populates="leaves")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["employee"] = "{} {}".format(self.employee.first_name,
                                              self.employee.last_name)
        date_format = "%Y-%m-%d"  # You can adjust this format based on your actual date format
        start_date = self.start_date
        end_date = self.end_date
        if type(start_date) == str:
            # Convert strings to datetime objects
            start_date = datetime.strptime(self.start_date, date_format)
        else:
            new_dict['start_date'] = self.start_date.strftime('%Y-%m-%d')
        if type(end_date) == str:
            # Convert strings to datetime objects
            end_date = datetime.strptime(self.end_date, date_format)
        else:
            new_dict['end_date'] = self.end_date.strftime('%Y-%m-%d')
        delta = end_date - start_date
        new_dict["duration"] = str(delta.days + 1) + " days"
        return new_dict
