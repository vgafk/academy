from typing import List, Optional

from sqlalchemy import select
from db.base import get_session
from db.models import Student


async def get_students() -> Student:
    async with get_session() as session:
        query = select(Student).order_by(Student.surname)
        result = (await session.execute(query)).scalars().all()
        return result


async def get_group_students(group_id: int) -> Student:
    async with get_session() as session:
        query = select(Student).where(Student.group_id == group_id) .order_by(Student.surname)
        result = (await session.execute(query)).scalars().all()
        return result


async def get_user_student_data(user_id: int) -> Student:
    async with get_session() as session:
        query = select(Student).where(Student.user_id == user_id).order_by(Student.id.desc())
        result = (await session.execute(query)).scalars().first()
        return result


async def get_student_data(student_id: int) -> Student:
    async with get_session() as session:
        query = select(Student).where(Student.id == student_id).order_by(Student.id.desc())
        result = (await session.execute(query)).scalars().first()
        return result


# async def add_student(student: Dict[str, str]) -> Any:
#     async with get_session() as session:
#         try:
#             new_user = {
#                 'surname': student['surname'],
#                 'name': student['name'],
#                 'middle_name': student['middle_name'],
#                 'snils': student['snils'],
#                 'inn': student['inn'],
#                 'email': student['email'],
#                 'phone': student['phone'],
#                 'study_year': int(student['study_year'])
#             }
#             query = insert(User).values(new_user)
#             user_id = (await session.execute(query)).lastrowid
#
#             new_student_data = {
#                 'user_id': user_id,
#                 'group_id': student['group_id'],
#             }
#             query_data = insert(StudentData).values(new_student_data)
#             await session.execute(query_data)
#
#             await session.commit()
#
#         except IntegrityError:
#             session.rollback()