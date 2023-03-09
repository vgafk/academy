from typing import List, Dict

from fastapi import APIRouter, HTTPException

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select, insert


router = APIRouter(prefix='/groups', tags=['Educational_forms'])


# ==================== routers =======================
@router.post('/', response_model=api_models.Groups)
async def create(group: api_models.Groups) -> api_models.Groups:
    return await create_group(group)


@router.get('/', response_model=List[api_models.Groups])
async def get_all() -> List[api_models.Groups]:
    return await get_groups()


@router.get('/{record_id}', response_model=api_models.Groups | Dict[str, str])
async def get_by_id(record_id: int) -> api_models.Groups | Dict[str, str]:
    return await get_group_by_id(record_id)


# ==================== resolvers =======================
async def create_group(new_group: api_models.Groups) -> api_models.Groups:
    group = sql_models.Groups(**new_group.to_filter_dict())
    async with get_session() as session:
        session.add(group)
        await session.commit()
        return api_models.Groups(**group.to_filter_dict())


async def get_groups() -> List[api_models.Groups]:
    stmt = select(sql_models.Groups)
    async with get_session() as session:
        groups_source = (await session.execute(stmt)).scalars().all()
        groups = [api_models.Groups(**group.to_filter_dict()) for group in groups_source]
        return groups


async def get_group_by_id(record_id: int) -> api_models.Groups:
    async with get_session() as session:
        group = await session.get(sql_models.Groups, record_id)
        if group:
            return api_models.Groups(**group.to_filter_dict())
        else:
            raise HTTPException(status_code=404, detail="Item not found")
