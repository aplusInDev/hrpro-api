#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from os import getenv


class Job(BaseModel, Base):
    """Job class"""
    __tablename__ = 'jobs'

    company_id = Column(String(50),
                        ForeignKey('companies.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    info = Column(Text, nullable=True)
    
    if getenv('HRPRO_TYPE_STORAGE') == 'db':
        company = relationship("Company", back_populates="jobs")
        employees = relationship("Employee", back_populates="job",
                               cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes a new instance"""
        super().__init__(*args, **kwargs)
