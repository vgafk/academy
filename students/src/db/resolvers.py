import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy import select, insert, delete, and_
from db.base import get_session
from db.models import Student, Absents


async def get_students() -> List[Student]:
    async with get_session() as session:
        query = select(Student).order_by(Student.surname)
        result = (await session.execute(query)).scalars().all()
        return result


async def get_group_students(group_id: int) -> List[Student]:
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


async def get_absents(student_id: int) -> List[Absents]:
    async with get_session() as session:
        query = select(Absents).where(Absents.student_id == student_id).order_by(Absents.date.desc())
        result = (await session.execute(query)).scalars().all()
        return result


async def add_student(student: Dict[str, str]) -> Any:
    async with get_session() as session:
        query = insert(Student).values(student)
        await session.execute(query)
        await session.commit()


async def add_apsent(student_id: int, date: str, number: int) -> None:
    async with get_session() as session:
        query = insert(Absents).values(
            student_id=student_id,
            date=datetime.datetime.strptime(date, "%Y-%m-%d"),
            number=number
        )
        await session.execute(query)
        await session.commit()


async def delete_apsent(student_id: int, date: str, number: int) -> None:
    async with get_session() as session:
        query = delete(Absents).where(and_(
            Absents.student_id == student_id,
            Absents.date == date,
            Absents.number == number)
        )
        await session.execute(query)
        await session.commit()
