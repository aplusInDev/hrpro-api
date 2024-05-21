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

    training = relationship("Training", back_populates="certificate")
    employee = relationship("Employee", back_populates="certificates")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["training"] = "http://localhost:5000/api/v1/trainings/{}".\
            format(self.training_id)
        new_dict["employee"] = "http://localhost:5000/api/v1/employees/{}".\
            format(self.employee_id)
        if "template" in new_dict:
            new_dict["template"] = "http://localhost:5000/api/v1/" +\
            "certificates/{}/template".format(self.id)
        return new_dict
