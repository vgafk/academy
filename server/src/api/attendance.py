from typing import List

from fastapi import APIRouter, HTTPException

from api import api_models
from sql import get_session
from sql import sql_models

from sqlalchemy import select, text

router = APIRouter(prefix='/attendance', tags=['Attendance'])


# ==================== routers =======================
@router.post('/')
async def create(attendances: List[api_models.Attendance]):
    await create_attendance(attendances)


@router.post('/update')
async def update(attendances: List[api_models.Attendance]):
    await update_attendance(attendances)


@router.post('/delete')
async def delete(attendances: List[api_models.Attendance]):
    await delete_attendance(attendances)


@router.get('/', response_model=List[api_models.Attendance])
async def get_by_group(group_id: int, week_number: int) -> List[api_models.Attendance]:
    return await get_attendance(group_id, week_number)


async def create_attendance(attendances: List[api_models.Attendance]):
    for attendance in attendances:
        new_attendance = sql_models.Attendance(**attendance.to_filter_dict())
        async with get_session() as session:
            session.add(new_attendance)
            await session.commit()


async def update_attendance(attendances: List[api_models.Attendance]):
    for attendance in attendances:
        stmt = text(f"""UPDATE attendance
        SET attendance_type_id = {attendance.attendance_type_id}
        WHERE id = {attendance.id}""")
        async with get_session() as session:
            await session.execute(stmt)
            await session.commit()


async def delete_attendance(attendances: List[api_models.Attendance]):
    for attendance in attendances:
        stmt = text(f"""DELETE FROM attendance
        WHERE id = {attendance.id}""")
        async with get_session() as session:
            await session.execute(stmt)
            await session.commit()


async def get_attendance(group_id: int, week_number: int):
    stmt = text(f"""SELECT A.id, A.student_id, A.schedule_id, attendance_type_id
    FROM attendance A
    INNER JOIN student_groups SG ON SG.student_id = A.student_id
    INNER JOIN `schedule` S ON A.schedule_id = S.id
    WHERE SG.group_id = {group_id} AND S.week_number = {week_number}""")

    async with get_session() as session:
        attendance_source = (await session.execute(stmt)).all()
        attendance_list = []
        for attendance in attendance_source:
            attendance_list.append(api_models.Attendance(id=attendance.id,
                                                         student_id=attendance.student_id,
                                                         schedule_id=attendance.schedule_id,
                                                         attendance_type_id=attendance.attendance_type_id))

        return attendance_list
