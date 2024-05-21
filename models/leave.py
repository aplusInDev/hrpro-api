#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship


leave_status = Enum("pending", "approved", "rejected", name="leave_status")


class Leave(BaseModel, Base):
    __tablename__= "leaves"

    employee_id = Column(String(50),
                        ForeignKey('employees.id', ondelete='CASCADE',
                                    onupdate='CASCADE'),
                        nullable=False
                        )
    leave_type = Column(String(50), nullable=False)
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(leave_status, nullable=False, default="pending")

    employee = relationship("Employee", back_populates="leaves")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["employee"] = "http://localhost:5000/api/v1/employees/{}".\
            format(self.employee_id)
        return new_dict
