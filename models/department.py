#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class Department(BaseModel, Base):
    __tablename__ = 'departments'

    name = Column(String(50), nullable=False)
    company_id = Column(String(50),
                        ForeignKey('companies.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    info = Column(Text, nullable=True)

    company = relationship("Company", back_populates="departments")
    employees = relationship("Employee", back_populates="department",
                                cascade="all, delete-orphan")
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["employees"] = [employee.to_dict() for employee in self.employees]
        return new_dict
