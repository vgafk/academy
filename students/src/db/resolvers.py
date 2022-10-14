from typing import List, Optional

from sqlalchemy import select
from db.base import get_session
from db.models import Student


async def get_students() -> Student:
    async with get_session() as session:
        query = select(Student).order_by(Student.surname)
        result = (await session.execute(query)).scalars().all()
        return result


async def get_user_student_data(user_id: int) -> Student:
    async with get_session() as session:
        query = select(Student).where(Student.user_id == user_id).order_by(Student.id.desc())
        result = (await session.execute(query)).scalars().first()
        return result


async def get_student_data(student_id: int) -> Student:
    async with get_session() as session:
        query = select(Student).where(Student.id == student_id).order_by(Student.id.desc())
        result = (await session.execute(query)).scalars().first()
        return result
