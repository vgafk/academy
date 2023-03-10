from typing import List

from fastapi import APIRouter, HTTPException

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select


router = APIRouter(prefix='/sub_groups', tags=['Sub_groups'])


# ==================== routers =======================
@router.post('/', response_model=api_models.SubGroups)
async def create(sub_group: api_models.SubGroups) -> api_models.SubGroups:
    return await create_sub_group(sub_group)


@router.get('/', response_model=List[api_models.SubGroups])
async def get_all() -> List[api_models.SubGroups]:
    return await get_sub_groups()


@router.get('/{record_id}', response_model=api_models.SubGroups)
async def get_by_id(record_id: int) -> api_models.SubGroups:
    return await get_sub_group_by_id(record_id)


# ==================== resolvers =======================
async def create_sub_group(new_sub_group: api_models.SubGroups) -> api_models.SubGroups:
    sub_group = sql_models.SubGroups(**new_sub_group.to_filter_dict())
    async with get_session() as session:
        session.add(sub_group)
        await session.commit()
        return api_models.SubGroups(**sub_group.to_filter_dict())


async def get_sub_groups() -> List[api_models.SubGroups]:
    stmt = select(sql_models.SubGroups)
    async with get_session() as session:
        sub_groups_source = (await session.execute(stmt)).scalars().all()
        sub_groups = [api_models.SubGroups(**sub_group.to_filter_dict()) for sub_group in sub_groups_source]
        return sub_groups


async def get_sub_group_by_id(record_id: int) -> api_models.SubGroups:
    async with get_session() as session:
        sub_group = await session.get(sql_models.SubGroups, record_id)
        if sub_group:
            return api_models.SubGroups(**sub_group.to_filter_dict())
        else:
            raise HTTPException(status_code=404, detail="Item not found")
