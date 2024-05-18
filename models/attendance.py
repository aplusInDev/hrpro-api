#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Time, Date, Enum
from sqlalchemy.orm import relationship
from os import getenv

# create enum with two values yes or no
absence_enum = Enum('Yes', 'No', name='absence_enum')
class Attendance(BaseModel, Base):
    """Attendance class"""
    __tablename__ = 'attendances'

    employee_id = Column(String(50),
                         ForeignKey('employees.id', ondelete='CASCADE',
                                    onupdate='CASCADE'),
                         nullable=False
                         )
    date= Column(Date, nullable=False)
    check_in = Column(Time, nullable=False)
    check_out = Column(Time, nullable=False)
    absent = Column(absence_enum, nullable=False)

    if getenv('HRPRO_TYPE_STORAGE') == 'db':
        employee = relationship("Employee", back_populates="attendances")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict['check_in'] = self.check_in.strftime('%H:%M:%S')
        new_dict['check_out'] = self.check_out.strftime('%H:%M:%S')
        new_dict['date'] = self.date.strftime('%Y-%m-%d')
        return new_dict
