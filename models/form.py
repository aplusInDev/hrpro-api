#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import (
    Column, String, ForeignKey, Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint


class Form(BaseModel, Base):
    """Form class"""
    __tablename__ = 'forms'
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    company_id = Column(
        String(50),
        ForeignKey('companies.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )
    __table_args__ = (
        UniqueConstraint('name', 'company_id', name='unique_form'),
    )
    company = relationship("Company", back_populates="forms")
    fields = relationship(
        "Field", back_populates="form", cascade="all, delete-orphan",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["fields"] = [field.to_dict() for field in self.fields]
        new_dict["company"] = "http://localhost:5000/api/v1/companies/{}".\
            format(self.company_id)
        new_dict["description"] = self.description if self.description else ""
        new_dict["uri"] = "http://localhost:5000/api/v1/forms/{}".format(self.id)
        return new_dict
