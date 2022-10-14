from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class Faculty(Base):
    __tablename__ = "faculties"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(length=20), nullable=False, unique=True)
    groups = relationship("Group", backref='faculty')


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(length=20), nullable=False, unique=True)
    full_name = Column(String(length=255), nullable=True)
    faculty_id = Column(ForeignKey("faculties.id"))





