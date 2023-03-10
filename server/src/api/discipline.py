from typing import List

from fastapi import APIRouter, HTTPException

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select


router = APIRouter(prefix='/disciplines', tags=['Disciplines'])


# ==================== routers =======================
@router.post('/', response_model=api_models.Discipline)
async def create(discipline: api_models.Discipline) -> api_models.Discipline:
    return await create_discipline(discipline)


@router.get('/', response_model=List[api_models.Discipline])
async def get_all() -> List[api_models.Discipline]:
    return await get_disciplines()


@router.get('/{record_id}', response_model=api_models.Discipline)
async def get_by_id(record_id: int) -> api_models.Discipline:
    return await get_discipline_by_id(record_id)


# ==================== resolvers =======================
async def create_discipline(new_discipline: api_models.Discipline) -> api_models.Discipline:
    discipline = sql_models.Discipline(**new_discipline.to_filter_dict())
    async with get_session() as session:
        session.add(discipline)
        await session.commit()
        return api_models.Discipline(**discipline.to_filter_dict())


async def get_disciplines() -> List[api_models.Discipline]:
    stmt = select(sql_models.Discipline)
    async with get_session() as session:
        disciplines_source = (await session.execute(stmt)).scalars().all()
        disciplines = [api_models.Discipline(**discipline.to_filter_dict()) for discipline in disciplines_source]
        return disciplines


async def get_discipline_by_id(record_id: int) -> api_models.Discipline:
    async with get_session() as session:
        discipline = await session.get(sql_models.Discipline, record_id)
        if discipline:
            return api_models.Discipline(**discipline.to_filter_dict())
        else:
            raise HTTPException(status_code=404, detail="Item not found")
