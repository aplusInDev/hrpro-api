#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import (
    Column, String, Date,
    LargeBinary, ForeignKey
    )
from sqlalchemy.orm import relationship


class Certificate(BaseModel, Base):
    """ training certificate """

    __tablename__ = 'certificates'

    training_id = Column(String(50),
                        ForeignKey('trainings.id', ondelete='CASCADE',
                                    onupdate='CASCADE'),
                        nullable=True
                        )
    employee_id = Column(String(50),
                        ForeignKey('employees.id', ondelete='CASCADE',
                                    onupdate='CASCADE'),
                        nullable=False
                        )
    institution = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    template = Column(LargeBinary, nullable=True)
    cssText = Column(String(128), nullable=True)

    training = relationship("Training", back_populates="certificates")
    employee = relationship("Employee", back_populates="certificates")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["training"] = self.training.to_dict()
        new_dict["employee"] = self.employee.to_dict()
        return new_dict
