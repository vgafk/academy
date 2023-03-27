from datetime import datetime
from typing import List
from uuid import uuid4

from sqlalchemy import String, DateTime, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .local_base import Base


class EducationalForms(Base):
    __tablename__ = 'educational_forms'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False)

    group: Mapped[List['Groups']] = relationship(back_populates='educational_form', cascade='all')


#
class Faculty(Base):
    __tablename__ = 'faculties'
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    group: Mapped[List["Groups"]] = relationship(back_populates='faculty', cascade='all')


class Groups(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    delete_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    faculty_id: Mapped[int] = mapped_column(ForeignKey('faculties.id'), nullable=False)
    educational_form_id: Mapped[int] = mapped_column(ForeignKey('educational_forms.id'))

    faculty: Mapped[List['Faculty']] = relationship(back_populates='group')
    educational_form: Mapped["EducationalForms"] = relationship(back_populates='group')
    student_groups: Mapped['StudentGroups'] = relationship(back_populates="group", cascade='all')
    schedule: Mapped[List["Schedule"]] = relationship(back_populates='group', cascade='all')

    # def to_dict(self):
    #     return {"id": self.id, "name": self.name, "educational_form_id": self.educational_form_id,
    #             "faculty_id": self.faculty_id}


class SubGroups(Base):
    __tablename__ = 'subgroups'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    comments: Mapped[str] = mapped_column(String(500), nullable=True)

    student_subgroups: Mapped[List["StudentSubgroups"]] = relationship(back_populates='subgroup', cascade='all', )
    schedule: Mapped[List["Schedule"]] = relationship(back_populates='subgroup', cascade='all')


class Students(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(255), nullable=True)
    snils: Mapped[str] = mapped_column(String(12), nullable=True)

    student_groups: Mapped[List['StudentGroups']] = relationship(back_populates="student", cascade='all')
    student_subgroups: Mapped[List['StudentSubgroups']] = relationship(back_populates="student", cascade='all')
    add_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    attendance: Mapped[List['Attendance']] = relationship(back_populates='student', cascade='all')


class StudentGroups(Base):
    __tablename__ = 'student_groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    add_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    remove_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    praepostor: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    student: Mapped["Students"] = relationship(back_populates='student_groups')
    group: Mapped["Groups"] = relationship(back_populates='student_groups', cascade='all')


class StudentSubgroups(Base):
    __tablename__ = 'student_subgroups'
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    subgroup_id: Mapped[int] = mapped_column(ForeignKey("subgroups.id"), nullable=True)

    student: Mapped["Students"] = relationship(back_populates='student_subgroups')
    subgroup: Mapped["SubGroups"] = relationship(back_populates='student_subgroups', cascade='all')


class Teachers(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(255), nullable=True)

    teacher_schedule: Mapped[List["TeacherSchedule"]] = relationship(back_populates='teacher', cascade='all')


class TeacherSchedule(Base):
    __tablename__ = 'teacher_schedule'
    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    schedule_id: Mapped[int] = mapped_column(ForeignKey('schedule.id'))

    teacher: Mapped["Teachers"] = relationship(back_populates='teacher_schedule')
    schedule: Mapped[List["Schedule"]] = relationship(back_populates='teacher_schedule', cascade='all')


class Discipline(Base):
    __tablename__ = 'disciplines'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    schedule: Mapped[List["Schedule"]] = relationship(back_populates='discipline', cascade='all')


class Schedule(Base):
    __tablename__ = 'schedule'
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    week_number: Mapped[int] = mapped_column(Integer)
    number_in_day: Mapped[int] = mapped_column(Integer)
    discipline_id: Mapped[int] = mapped_column(ForeignKey('disciplines.id'))
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    subgroup_id: Mapped[int] = mapped_column(ForeignKey('subgroups.id'), nullable=True)

    discipline: Mapped["Discipline"] = relationship(back_populates='schedule')
    group: Mapped["Groups"] = relationship(back_populates='schedule')
    subgroup: Mapped["SubGroups"] = relationship(back_populates='schedule')
    teacher_schedule: Mapped[List["TeacherSchedule"]] = relationship(back_populates='schedule', cascade='all')

    attendance: Mapped[List['Attendance']] = relationship(back_populates='schedule', cascade='all')


class AttendanceTypes(Base):
    __tablename__ = 'attendance_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    attendance: Mapped[List['Attendance']] = relationship(back_populates='attendance_type', cascade='all')


class Attendance(Base):
    __tablename__ = 'attendance'
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    schedule_id: Mapped[int] = mapped_column(ForeignKey('schedule.id'))
    attendance_type_id: Mapped[int] = mapped_column(ForeignKey('attendance_types.id'))

    student: Mapped['Students'] = relationship(back_populates='attendance')
    schedule: Mapped['Schedule'] = relationship(back_populates='attendance')
    attendance_type: Mapped['AttendanceTypes'] = relationship(back_populates='attendance')
