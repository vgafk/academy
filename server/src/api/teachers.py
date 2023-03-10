from typing import List

from fastapi import APIRouter, HTTPException

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select


router = APIRouter(prefix='/teachers', tags=['Teachers'])


# ==================== routers =======================
@router.post('/', response_model=api_models.Teachers)
async def create(teacher: api_models.Teachers) -> api_models.Teachers:
    return await create_teacher(teacher)


@router.get('/', response_model=List[api_models.Teachers])
async def get_all() -> List[api_models.Teachers]:
    return await get_teachers()


@router.get('/{record_id}', response_model=api_models.Teachers)
async def get_by_id(record_id: int) -> api_models.Teachers:
    return await get_teacher_by_id(record_id)


# ==================== resolvers =======================
async def create_teacher(new_teacher: api_models.Teachers) -> api_models.Teachers:
    teacher = sql_models.Teachers(**new_teacher.to_filter_dict())
    async with get_session() as session:
        session.add(teacher)
        await session.commit()
        return api_models.Teachers(**teacher.to_filter_dict())


async def get_teachers() -> List[api_models.Teachers]:
    stmt = select(sql_models.Teachers)
    async with get_session() as session:
        teachers_source = (await session.execute(stmt)).scalars().all()
        teachers = [api_models.Teachers(**teacher.to_filter_dict()) for teacher in teachers_source]
        return teachers


async def get_teacher_by_id(record_id: int) -> api_models.Teachers:
    async with get_session() as session:
        teacher = await session.get(sql_models.Teachers, record_id)
        if teacher:
            return api_models.Teachers(**teacher.to_filter_dict())
        else:
            raise HTTPException(status_code=404, detail="Item not found")
