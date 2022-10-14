from typing import List

from sqlalchemy import select, or_, insert

from db.base import get_session
from db.models import User


async def get_users() -> List[User]:
    query = select(User).order_by(User.id)
    async with get_session() as session:
        result = (await session.execute(query)).scalars().all()
        return result


async def get_user(user_id: int, login: str) -> User:
    async with get_session() as session:
        query = select(User).where(or_(User.id == user_id, User.login == login))
        result = (await session.execute(query)).scalars().first()
        return result


async def add_user(login: str, password: str) -> bool:
    user = await get_user(login=login, user_id=0)
    if user:
        return False

    new_user = {'login': login, 'password': password}
    query = insert(User).values(new_user)
    async with get_session() as session:
        await session.execute(query)
        await session.commit()
        return True
