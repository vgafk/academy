from contextlib import asynccontextmanager
from typing import AsyncGenerator
from abc import abstractmethod

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from settings import settings

engine = create_async_engine(f"{settings.LOCAL_BASE_DRIVER}://{settings.LOCAL_BASE_USER_NAME}:"
                             f"{settings.LOCAL_BASE_USER_PASSWORD}@{settings.LOCAL_BASE_HOST}/"
                             f"{settings.LOCAL_BASE_NAME}", echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):

    def to_filter_dict(self):
        return {key: value for key, value in self.__dict__.items() if key not in ['_sa_instance_state']}


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()