from typing import List, Dict

from fastapi import APIRouter

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select, insert

router = APIRouter(prefix='/groups', tags=['Groups'])


# ==================== routers =======================
@router.get('/')
async def get_all() -> List[api_models.Groups]:
    return await get_groups()


# @router.get('/{id}')
# async def get(record_id: int) -> api_models.Groups | None:
#     await get_groups(record_id)

@router.post('/')
async def all(group: api_models.Groups) -> dict:
    return await create_group(group)

# ==================== resolvers =======================


async def get_groups(record_id: int = None):
    stmt = select(sql_models.Groups)
    # print(stmt)
    # if record_id:
    #     stmt = stmt.filter(sql_models.Groups.id == record_id)
    #     print(stmt)
    async with get_session() as session:
        result = (await session.execute(stmt)).all()
        for res in result:
            print(res)
    return []


async def create_group(group: api_models.Groups) -> Dict[str, str]:
    stmt = insert(sql_models.Groups).values(name=group.name, educational_form_id=group.educational_form_id,
                                            faculty_id=group.faculty_id)
    async with get_session() as session:
        result = (await session.execute(stmt)).all()
        session.commit()

    return {'code': '200', 'inserted_id': result.inserted_primary_key}
