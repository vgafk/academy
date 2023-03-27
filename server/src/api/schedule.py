from typing import List

from fastapi import APIRouter, HTTPException
from datetime import date, timedelta
from isoweek import Week

from api import api_models
from api.teachers import get_teacher_by_id
from sql import sql_models, get_session

from sqlalchemy import select, text
from sqlalchemy.engine import row

router = APIRouter(prefix='/schedule', tags=['Schedule'])


# ==================== routers =======================
# @router.post('/', response_model=api_models.Schedule)
# async def create(schedule: api_models.Schedule) -> api_models.Schedule:
#     return await create_schedule(schedule)


@router.post('/')
async def create(schedule: api_models.ScheduleQuery) -> int:
    return await create_week_schedule(schedule)


@router.get('/', response_model=List[api_models.Schedule])
async def get_all(week_number: int, group_id: int) -> List[api_models.Schedule]:
    return await get_schedule(week_number, group_id)


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


async def create_lesson_schedule(current_date: date, number_in_day: int, group_id: int, week_number: int):
    stmt = text(f"""INSERT INTO schedule(date, number_in_day, discipline_id, group_id, week_number) 
                   VALUES('{current_date.strftime('%Y-%m-%d')}', {number_in_day}, 1, {group_id}, {week_number})""")
    async with get_session() as session:
        result = (await session.execute(stmt))
        await session.commit()
    return result.lastrowid


async def create_teacher_schedule(teacher_id: int, lesson_id: int):
    stmt = text(f"""INSERT INTO teacher_schedule(teacher_id, schedule_id)
                                    VALUES({teacher_id}, {lesson_id})""")
    async with get_session() as session:
        result = (await session.execute(stmt))
        await session.commit()
    return result.lastrowid


async def create_week_schedule(schedule: api_models.ScheduleQuery):
    print("create_week_schedule")
    # schedule = sql_models.Schedule(**new_schedule.to_filter_dict())
    async with get_session() as session:
        monday_date = get_week_start_date(schedule.week_number)
        for day in range(5):
            current_date = monday_date + timedelta(days=day)
            for number_in_day in range(1, 6):
                lesson_id = await create_lesson_schedule(current_date, number_in_day, schedule.group_id,
                                                         schedule.week_number)
                teacher_schedule_id = await create_teacher_schedule(1, lesson_id)
        return 200


# async def get_schedule(params: api_models.ScheduleQuery) -> List[api_models.Schedule]:
async def get_schedule(week_number: int, group_id: int) -> List[api_models.Schedule]:
    # stmt = select(sql_models.Schedule.__table__.c['id', 'date', 'number_in_day', 'week_number', 'discipline_id',
    #                                               'group_id'], sql_models.Discipline.__table__.c['name'],
    #               sql_models.Groups.__table__.c['name']).join(sql_models.Discipline).join(sql_models.Groups)

    stmt = text(f"""SELECT S.id id, S.date, S.number_in_day, G.name group_name,
    GROUP_CONCAT(T.surname SEPARATOR ';') teachers, S.week_number, S.group_id
    FROM `schedule` S
    INNER JOIN disciplines D ON S.discipline_id = D.id
    INNER JOIN `groups` G ON S.group_id = G.id
    LEFT JOIN subgroups SG ON S.subgroup_id = SG.id
    INNER JOIN teacher_schedule ON teacher_schedule.schedule_id = S.id
    INNER JOIN teachers T ON teacher_schedule.teacher_id = T.id
    WHERE S.week_number = {week_number} AND G.id = {group_id}
    GROUP BY S.id, S.date, S.number_in_day, G.name, S.group_id
    ORDER BY S.date, S.number_in_day""")

    # if params.group_id:
    #     stmt = stmt.where(sql_models.Schedule.group_id == params.group_id)
    # if params.week_number:
    #     stmt = stmt.where(sql_models.Schedule.week_number == params.week_number)
    # if params.schedule_date:
    #     stmt = stmt.where(sql_models.Schedule.date == params.schedule_date)

    async with get_session() as session:
        schedule_source = (await session.execute(stmt)).all()
        schedule_list = []
        for schedule in schedule_source:
            schedule_list.append(api_models.Schedule(id=schedule.id,
                                                     date=schedule.date,
                                                     number_in_day=schedule.number_in_day,
                                                     week_number=schedule.week_number,
                                                     group_id=schedule.group_id,
                                                     group_name=schedule.group_name,
                                                     teachers=schedule.teachers))
        return schedule_list


async def get_schedule_by_id(record_id: int) -> api_models.Schedule:
    async with get_session() as session:
        schedule = await session.get(sql_models.Schedule, record_id)
        if schedule:
            return api_models.Schedule(**schedule.to_filter_dict())
        else:
            raise HTTPException(status_code=404, detail="Item not found")



def get_week_start_date(week_number: int) -> date:
    return Week(date.today().year, week_number).monday()