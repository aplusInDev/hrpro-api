#!/usr/bin/env python3

from models import BaseModel, Base
# from models import Employee
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from os import getenv


class Company(BaseModel, Base):
    """Company class"""
    __tablename__ = 'companies'


    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    address = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(50), nullable=True)

    if getenv('HRPRO_TYPE_STORAGE') == 'db':
        departments = relationship("Department", back_populates="company",
                                   cascade="all, delete-orphan")
        employees = relationship("Employee", back_populates="company",
                                 cascade="all, delete-orphan")
        jobs = relationship("Job", back_populates="company",
                            cascade="all, delete-orphan")
        forms = relationship("Form", back_populates="company",
                             cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes a new instance"""
        super().__init__(*args, **kwargs)
