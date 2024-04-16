#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from os import getenv


class Department(BaseModel, Base):
    __tablename__ = 'departments'

    company_id = Column(String(50),
                        ForeignKey('companies.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    info = Column(Text, nullable=True)

    if getenv('HRPRO_TYPE_STORAGE') == 'db':
        company = relationship("Company", back_populates="departments")
        employees = relationship("Employee", back_populates="department",
                                 cascade="all, delete-orphan")
        
        def to_dict(self):
            new_dict = super().to_dict().copy()
            new_dict["employees"] = [employee.to_dict() for employee in self.employees]
            return new_dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
