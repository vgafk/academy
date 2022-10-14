from sqlalchemy import Column, String, Integer

from db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    login = Column(String(length=100), nullable=False)
    password = Column(String(length=255), nullable=False)
