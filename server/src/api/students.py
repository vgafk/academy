from typing import List

from fastapi import APIRouter, HTTPException

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select


router = APIRouter(prefix='/students', tags=['Students'])


# ==================== routers =======================
@router.post('/', response_model=api_models.Students)
async def create(student: api_models.Students) -> api_models.Students:
    return await create_student(student)


@router.get('/', response_model=List[api_models.Students])
async def get_all(parameters: api_models.StudentQuery) -> List[api_models.Students]:
    return await get_students(parameters)


@router.get('/{record_id}', response_model=api_models.Students)
async def get_by_id(record_id: int) -> api_models.Students:
    return await get_student_by_id(record_id)


# ==================== resolvers =======================
async def create_student(new_student: api_models.Students) -> api_models.Students:
    student = sql_models.Students(**new_student.to_filter_dict())

    if new_student.group_id:
        student.student_groups = [sql_models.StudentGroups(group_id=new_student.group_id,
                                                           sub_group_id=new_student.sub_group_id)]

    async with get_session() as session:
        session.add(student)
        await session.commit()
        return api_models.Students(**student.to_filter_dict())


async def get_students(parameters: api_models.StudentQuery) -> List[api_models.Students]:
    stmt = select(sql_models.Students, sql_models.StudentGroups).join(sql_models.StudentGroups)
    stmt = stmt.where(sql_models.Students.surname == parameters.surname) if parameters.surname else stmt
    stmt = stmt.where(sql_models.Students.name == parameters.name) if parameters.name else stmt
    stmt = stmt.where(sql_models.Students.middle_name == parameters.middle_name) if parameters.middle_name else stmt
    stmt = stmt.where(sql_models.StudentGroups.sub_group_id == parameters.sub_group_id) \
        if parameters.sub_group_id else stmt

    async with get_session() as session:
        students_source = (await session.execute(stmt)).all()
        print(students_source)
        students = [api_models.Students(**student[0].to_filter_dict(), group_id=student[1].group_id,
                                        sub_group_id=student[1].sub_group_id) for student in students_source]
        return students


async def get_student_by_id(record_id: int) -> api_models.Students:
    stmt = select(sql_models.Students, sql_models.StudentGroups)\
        .join(sql_models.StudentGroups).where(sql_models.Students.id == record_id)
    async with get_session() as session:
        student, groups = (await session.execute(stmt)).one()
        if student:
            return api_models.Students(**student.to_filter_dict(), group_id=groups.group_id,
                                       sub_group_id=groups.sub_group_id)
        else:
            raise HTTPException(status_code=404, detail="Item not found")
