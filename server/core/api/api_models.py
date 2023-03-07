from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EducationalForms(BaseModel):
    id: Optional[int] = None
    name: str


class Faculty(BaseModel):
    id: Optional[int] = None
    full_name: str
    name: str


class Groups(BaseModel):
    id: Optional[int] = None
    name: str
    educational_form_id: int
    faculty_id: int


class SubGroups(BaseModel):
    id: Optional[int] = None
    name: str
    comments: Optional[str] = None
    group_id: int


class Students(BaseModel):
    id: Optional[int] = None
    surname: str
    name: str
    middle_name: Optional[str] = None
    snils: Optional[str] = None


class StudentGroups(BaseModel):
    id: Optional[int] = None
    remove_date: Optional[datetime] = None
    student_id: int
    group_id: int
    sub_group_id: Optional[str]


class Teachers(BaseModel):
    id: Optional[int] = None
    surname: str
    name: Optional[str] = None
    middle_name: Optional[str] = None


class Discipline(BaseModel):
    id: Optional[int] = None
    name: str


class Schedule(BaseModel):
    id: Optional[int] = None
    date: datetime
    number_in_day: int
    teacher_id: int
    discipline_id: int
    group_id: int
    sub_group_id: int


class AttendanceTypes(BaseModel):
    id: Optional[int] = None
    name: str


class Attendance(BaseModel):
    id: Optional[int] = None
    student_id: int
    schedule_id: int
    attendance_type_id: int