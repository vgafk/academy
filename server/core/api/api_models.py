from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ValidateModel(BaseModel):

    def to_filter_dict(self):
        return self.__dict__
        # return {key: value for key, value in self.__dict__.items() if key not in ['_sa_instance_state']}


class EducationalForms(ValidateModel):
    id: Optional[int] = None
    name: str


class Faculty(ValidateModel):
    id: Optional[int] = None
    full_name: str
    name: str


class Groups(ValidateModel):
    id: Optional[int] = None
    name: str
    educational_form_id: int
    faculty_id: int


class SubGroups(ValidateModel):
    id: Optional[int] = None
    name: str
    comments: Optional[str] = None
    group_id: int


class Students(ValidateModel):
    id: Optional[int] = None
    surname: str
    name: str
    middle_name: Optional[str] = None
    snils: Optional[str] = None


class StudentGroups(ValidateModel):
    id: Optional[int] = None
    remove_date: Optional[datetime] = None
    student_id: int
    group_id: int
    sub_group_id: Optional[str]


class Teachers(ValidateModel):
    id: Optional[int] = None
    surname: str
    name: Optional[str] = None
    middle_name: Optional[str] = None


class Discipline(ValidateModel):
    id: Optional[int] = None
    name: str


class Schedule(ValidateModel):
    id: Optional[int] = None
    date: datetime
    number_in_day: int
    teacher_id: int
    discipline_id: int
    group_id: int
    sub_group_id: int


class AttendanceTypes(ValidateModel):
    id: Optional[int] = None
    name: str


class Attendance(ValidateModel):
    id: Optional[int] = None
    student_id: int
    schedule_id: int
    attendance_type_id: int