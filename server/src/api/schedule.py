from datetime import date
from typing import List

from fastapi import APIRouter, HTTPException

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select


router = APIRouter(prefix='/schedule', tags=['Schedule'])


# ==================== routers =======================
@router.post('/', response_model=api_models.Schedule)
async def create(schedule: api_models.Schedule) -> api_models.Schedule:
    return await create_schedule(schedule)


@router.get('/', response_model=List[api_models.Schedule])
async def get_all(params: api_models.ScheduleQuery) -> List[api_models.Schedule]:
    return await get_schedule(params)


@router.get('/{record_id}', response_model=api_models.Schedule)
async def get_by_id(record_id: int) -> api_models.Schedule:
    return await get_schedule_by_id(record_id)


# ==================== resolvers =======================
async def create_schedule(new_schedule: api_models.Schedule) -> api_models.Schedule:
    schedule = sql_models.Schedule(**new_schedule.to_filter_dict())
    async with get_session() as session:
        session.add(schedule)
        await session.commit()
        return api_models.Schedule(**schedule.to_filter_dict())


async def get_schedule(params: api_models.ScheduleQuery) -> List[api_models.Schedule]:
    stmt = select(sql_models.Schedule)
    if params.group_id:
        stmt = stmt.where(sql_models.Schedule.group_id == params.group_id)
    if params.week_number:
        stmt = stmt.where(sql_models.Schedule.week_number == params.week_number)
    if params.schedule_date:
        stmt = stmt.where(sql_models.Schedule.date == params.schedule_date)

    async with get_session() as session:
        schedule_source = (await session.execute(stmt)).scalars().all()
        schedule = [api_models.Schedule(**schedule.to_filter_dict()) for schedule in schedule_source]
        return schedule


async def get_schedule_by_id(record_id: int) -> api_models.Schedule:
    async with get_session() as session:
        schedule = await session.get(sql_models.Schedule, record_id)
        if schedule:
            return api_models.Schedule(**schedule.to_filter_dict())
        else:
            raise HTTPException(status_code=404, detail="Item not found")


