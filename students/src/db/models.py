from sqlalchemy import Column, Integer, String

from db.base import Base


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    group_id = Column(Integer, index=True)
    surname = Column(String(length=255), nullable=False)
    name = Column(String(length=255), nullable=False)
    middle_name = Column(String(length=255), nullable=True)
    snils = Column(String(length=20), nullable=True, unique=True)
    inn = Column(String(length=20), nullable=True)
    email = Column(String(length=255), nullable=True)
    phone = Column(String(length=15), nullable=True)
    study_year = Column(Integer, nullable=False)
