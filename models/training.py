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
                        nullable=False
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
    evaluations = relationship("Evaluation", back_populates="training")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict().copy()
        new_dict["company"] = "http://localhost:5000/api/v1/companies/{}".\
            format(self.company_id)
        if self.department_id:
            new_dict["department"] = "http://localhost:5000/api/v1/departments/{}".\
                format(self.department_id)
        if self.job_id:
            new_dict["job"] = "http://localhost:5000/api/v1/jobs/{}".\
                format(self.job_id)
        if self.trainer_id:
            new_dict["trainer"] = "http://localhost:5000/api/v1/employees/{}".\
                format(self.trainer_id)
        new_dict["trainees"] = {
            trainee.first_name + " " + trainee.last_name:
            "http://localhost:5000/api/v1/employees/" + trainee.id
            for trainee in self.trainees
            }
        new_dict["evaluations"] = [
            {"traineee": "Anonimous" if evaluation.anonimous 
                else evaluation.employee.first_name + " " +\
                evaluation.employee.last_name,
             "score": evaluation.score,
             "feedback": evaluation.feedback,
             "uri": "http://localhost:5000/api/v1/evaluations/" + evaluation.id
             } for evaluation in self.evaluations
            ]
        new_dict["uri"] = "http://localhost:5000/api/v1/trainings/{}".\
            format(self.id)
        try:
            new_dict["start_date"] = self.start_date.strftime("%Y-%m-%d")
            new_dict["end_date"] = self.end_date.strftime("%Y-%m-%d")
        except Exception:
            pass
        return new_dict
