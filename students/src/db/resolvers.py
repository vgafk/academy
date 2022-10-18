from typing import List, Optional, Dict, Any

from sqlalchemy import select, insert
from db.base import get_session
from db.models import Student


async def get_students() -> Student:
    async with get_session() as session:
        query = select(Student).order_by(Student.surname)
        result = (await session.execute(query)).scalars().all()
        return result


async def get_group_students(group_id: int) -> Student:
    async with get_session() as session:
        query = select(Student).where(Student.group_id == group_id) .order_by(Student.surname)
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


async def add_student(student: Dict[str, str]) -> Any:
    async with get_session() as session:
        query = insert(Student).values(student)
        await session.execute(query)
        await session.commit()
#
