from typing import List, Optional, Dict

from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from db.base import get_session
from db.models import Group, Faculty


async def get_faculties() -> List[Faculty]:
    async with get_session() as session:
        query = select(Faculty).order_by(Faculty.name)
        result = (await session.execute(query)).scalars().all()
        return result


async def get_faculty(faculty_id: int) -> Faculty:
    async with get_session() as session:
        query = select(Faculty).where(Faculty.id == faculty_id)
        result = (await session.execute(query)).scalars().first()
        return result


async def get_groups() -> List[Group]:
    async with get_session() as session:
        query = select(Group).order_by(Group.name)
        result = (await session.execute(query)).scalars().all()
        return result


async def get_group(group_id: int) -> Group:
    async with get_session() as session:
        query = select(Group).where(Group.id == group_id)
        result = (await session.execute(query)).scalars().first()
        return result


async def get_groups_by_faculty(faculty_id: int) -> List[Group]:
    async with get_session() as session:
        query = select(Group).where(Group.faculty_id == faculty_id)
        result = (await session.execute(query)).scalars().all()
        return result


async def add_group(new_group: Dict[str, str]):
    async with get_session() as session:
        try:
            query = insert(Group).values(new_group)
            print(query)
            await session.execute(query)
            await session.commit()
        except IntegrityError:
            pass