#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import (
    Column, String, Table,
    Text, Date, ForeignKey,
    )
from sqlalchemy.orm import relationship


training_trainees = Table('training_trainees', Base.metadata,
                          Column('training_id', String(50),
                                 ForeignKey('trainings.id',
                                            ondelete='CASCADE',
                                            onupdate='CASCADE'
                                            ),
                                 primary_key=True
                                ),
                          Column('employee_id', String(50),
                                 ForeignKey('employees.id',
                                            ondelete='CASCADE',
                                            onupdate='CASCADE'
                                            ),
                                 primary_key=True
                                )
                    )


class Training(BaseModel, Base):

    __tablename__ = 'trainings'

    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    company_id = Column(String(50),
                        ForeignKey('companies.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    department_id = Column(String(50),
                        ForeignKey('departments.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    job_id = Column(String(50),
                        ForeignKey('jobs.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    trainer_id = Column(String(50),
                        ForeignKey('employees.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )

    company = relationship("Company", back_populates="trainings")
    department = relationship("Department", back_populates="trainings")
    job = relationship("Job", back_populates="trainings")
    trainer = relationship("Employee", back_populates="trainings")
    trainees = relationship("Employee", secondary=training_trainees,
                            back_populates="trainings")
    certificate = relationship("Certificate", back_populates="training", uselist=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        return new_dict
