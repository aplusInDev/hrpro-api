#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Form(BaseModel, Base):
    """Form class"""
    __tablename__ = 'forms'

    name = Column(String(50), nullable=False)
    company_id = Column(String(50),
                        ForeignKey('companies.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    
    if getenv('HRPRO_TYPE_STORAGE') == 'db':
        company = relationship("Company", back_populates="forms")
        fields = relationship("Field", back_populates="form",
                              cascade="all, delete-orphan")
        
        def to_dict(self):
            new_dict = super().to_dict().copy()
            new_dict["fields"] = [field.to_dict() for field in self.fields]
            return new_dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
