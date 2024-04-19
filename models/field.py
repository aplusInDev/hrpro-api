#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Boolean, Text, Integer
from sqlalchemy.orm import relationship
from os import getenv


class Field(BaseModel, Base):
    """Field class"""
    __tablename__ = 'fields'

    form_id = Column(String(50),
                        ForeignKey('forms.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    fposition = Column(Integer, nullable=True)
    fname = Column(String(50), nullable=True)
    fdescription = Column(Text, nullable=True)
    ftype = Column(String(50), nullable=True, default="text")
    default_value = Column(String(50), nullable=True, default="")
    options = Column(String(50), nullable=True, default="[]")
    is_required = Column(Boolean, nullable=True, default=True)


    if getenv('HRPRO_TYPE_STORAGE') == 'db':
        form = relationship("Form", back_populates="fields")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
