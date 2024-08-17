#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import (
    Column, String, ForeignKey,
    Boolean, Text, Integer,
)
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint


class Field(BaseModel, Base):
    """Field class"""
    __tablename__ = 'fields'
    form_id = Column(
        String(50),
        ForeignKey('forms.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )
    position = Column(Integer, nullable=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(50), nullable=True, default="text")
    default_value = Column(String(50), nullable=True)
    options = Column(String(50), nullable=True)
    is_required = Column(Boolean, nullable=True, default=False)
    __table_args__ = (
        UniqueConstraint('form_id', 'name', name='unique_field'),
    )
    form = relationship("Form", back_populates="fields")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["form"] = self.form.name if self.form else ""
        new_dict["description"] = self.description if self.description else ""
        new_dict["options"] = eval(self.options) if self.options else []
        new_dict["uri"] = "http://localhost:5000/api/v1/fields/{}".format(self.id)
        new_dict["default_value"] = self.default_value\
            if self.default_value else ""
        return new_dict
