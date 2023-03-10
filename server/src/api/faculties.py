from typing import List

from fastapi import APIRouter, HTTPException

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select

router = APIRouter(prefix='/faculties', tags=['Faculties'])


# ==================== routers =======================
@router.post('/', response_model=api_models.Faculty)
async def create(faculty: api_models.Faculty) -> api_models.Faculty:
    return await create_faculty(faculty)


@router.get('/', response_model=List[api_models.Faculty])
async def get_all() -> List[api_models.Faculty]:
    return await get_faculties()


@router.get('/{record_id}', response_model=api_models.Faculty)
async def get_by_id(record_id: int) -> api_models.Faculty:
    return await get_faculty_by_id(record_id)


# ==================== resolvers =======================
async def create_faculty(new_faculty: api_models.Faculty) -> api_models.Faculty:
    faculty = sql_models.Faculty(**new_faculty.to_filter_dict())
    async with get_session() as session:
        session.add(faculty)
        await session.commit()
        return api_models.Faculty(**faculty.to_filter_dict())


async def get_faculties() -> List[api_models.Faculty]:
    stmt = select(sql_models.Faculty)
    async with get_session() as session:
        faculties_source = (await session.execute(stmt)).scalars().all()
        print(faculties_source)
        faculties = [api_models.Faculty(**faculty.to_filter_dict())
                     for faculty in faculties_source]
        return faculties


async def get_faculty_by_id(record_id: int) -> api_models.Faculty:
    async with get_session() as session:
        faculty = await session.get(sql_models.Faculty, record_id)
        if faculty:
            return api_models.Faculty(**faculty.to_filter_dict())
        else:
            raise HTTPException(status_code=404, detail="Item not found")
