#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class Job(BaseModel, Base):
    """Job class"""
    __tablename__ = 'jobs'

    title = Column(String(50), nullable=False)
    company_id = Column(String(50),
                        ForeignKey('companies.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    info = Column(Text, nullable=True)

    company = relationship("Company", back_populates="jobs")
    employees = relationship("Employee", back_populates="job",
                            cascade="all, delete-orphan")
    
    def __init__(self, *args, **kwargs):
        """Initializes a new instance"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["employees"] = [employee.to_dict() for employee in self.employees]
        return new_dict
