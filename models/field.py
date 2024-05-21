#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Boolean, Text, Integer
from sqlalchemy.orm import relationship


class Field(BaseModel, Base):
    """Field class"""
    __tablename__ = 'fields'

    form_id = Column(String(50),
                        ForeignKey('forms.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    position = Column(Integer, nullable=True)
    name = Column(String(50), nullable=True)
    description = Column(Text, default="")
    type = Column(String(50), nullable=True, default="text")
    default_value = Column(String(50), nullable=True, default="")
    options = Column(String(50), nullable=True, default="[]")
    is_required = Column(Boolean, nullable=True, default=True)

    form = relationship("Form", back_populates="fields")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["form"] = "http://localhost:5000/api/v1/forms/{}".\
            format(self.form_id)
        return new_dict
