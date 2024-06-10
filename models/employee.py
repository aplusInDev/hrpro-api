#!/usr/bin/env python3

from models import BaseModel, Base
from sqlalchemy import (
    Column, String, Date,
    ForeignKey, Text, Integer,
    )
from sqlalchemy.orm import relationship
from datetime import date


class Employee(BaseModel, Base):
    """Employee class"""
    __tablename__ = 'employees'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    leave_balance = Column(Integer, nullable=True, default=0)
    hire_date = Column(Date, nullable=True)
    company_id = Column(String(50),
                        ForeignKey('companies.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    job_id = Column(String(50),
                        ForeignKey('jobs.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    department_id = Column(String(50),
                        ForeignKey('departments.id', ondelete='CASCADE',
                                   onupdate='CASCADE'),
                        nullable=True
                        )
    info = Column(Text, nullable=True)

    department = relationship("Department", back_populates="employees")
    job = relationship("Job", back_populates="employees")
    company = relationship("Company", back_populates="employees")
    attendances = relationship("Attendance", back_populates="employee",
                                cascade="all, delete-orphan")
    absences = relationship("Absence", back_populates="employee",
                            cascade="all, delete-orphan")
    leaves = relationship("Leave", back_populates="employee",
                          cascade="all, delete-orphan")
    trainings = relationship("Training", secondary="training_trainees",
                            back_populates="trainees")
    evaluations = relationship("Evaluation", back_populates="employee",
                                cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="employee",
                                cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="employee",
                               cascade="all, delete-orphan")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "hire_date" not in kwargs:
            self.hire_date = date.today()

    def to_dict(self):
        new_dict = super().to_dict().copy()
        n_absences = len(self.absences)
        absences_days = self.calc_absences_days()
        justified_absences = self.calc_justefied_absences()
        justified_days = self.calc_justefied_absences_days()
        try:
            position_info = eval(self.job.info)
            position_info = {"job_" + k: v for k, v in position_info.items()}
            new_dict["position_info"] = position_info
        except Exception as err:
            print("error: ", str(err))
            pass
        try:
            department_info = eval(self.department.info)
            department_info = {
                "department_" + k: v for k, v in department_info.items()
                }
            new_dict["department_info"] = department_info
        except Exception as err:
            print("error: ", str(err))
            pass
        try:
            new_dict["info"] = eval(self.info)
        except Exception as err:
            print("error: ", str(err))
            pass
        new_dict["department"] = "http://localhost:5000/api/v1/departments/{}".\
            format(self.department_id)
        new_dict["job"] = "http://localhost:5000/api/v1/jobs/{}".\
            format(self.job_id)
        new_dict["company"] = "http://localhost:5000/api/v1/companies/{}".\
            format(self.company_id)
        new_dict["hire_date"] = self.hire_date.strftime("%Y-%m-%d")
        new_dict["uri"] = "http://localhost:5000/api/v1/employees/" + self.id
        new_dict["absences"] = n_absences
        new_dict["absences_total_days"] = absences_days
        new_dict["justified_absences"] = justified_absences
        new_dict["justified_absences_days"] = justified_days
        new_dict["unjustified_absences"] = n_absences - justified_absences
        new_dict["unjustified_absences_days"] = absences_days - justified_days
        return new_dict
    
    def calc_absences_days(self):
        """ calculate the total number of days an employee was absent
        """
        return sum([absence.to_dict()["n_days"] for absence in self.absences])
    
    def calc_justefied_absences(self):
        """ Calculate the total number of justefied absences
        """
        justified = 0
        for absence in self.absences:
            if absence.reason:
                justified += 1
        return justified
    
    def calc_justefied_absences_days(self):
        """ Calculate the total number of days an employee was absent
        and the absence was justified
        """
        return sum([absence.to_dict()["n_days"] for absence in self.absences
                    if absence.reason])
