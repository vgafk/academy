from typing import Optional, List

import strawberry
from strawberry.file_uploads import Upload

from api.types import SelectStudentResponse, StudentNotFound, Student
from db.resolvers import get_student_data, get_students, get_group_students, add_apsent, delete_apsent
from files.files_handel import FileHandler


@strawberry.type
class Query:

    @strawberry.field
    async def student(self, student_id: int) -> SelectStudentResponse:
        res = await get_student_data(student_id)
        if not res:
            return StudentNotFound
        else:
            return Student.from_instance(res)

    @strawberry.field
    async def students(self) -> List[Student]:
        res = await get_students()
        return [Student.from_instance(student) for student in res]

    @strawberry.field
    async def group_students(self, group_id: int) -> List[Student]:
        res = await get_group_students(group_id)
        return [Student.from_instance(student) for student in res]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def upload_students(self, file: Upload) -> str:
        await FileHandler.add_batch_students(data_bytes=await file.read())
        return '{"code": 200}'

    @strawberry.mutation
    async def add_apsent(self, student_id: int, date: str, number: int) -> str:
        await add_apsent(student_id=student_id, date=date, number=number)
        return '{"code": 200}'

    @strawberry.mutation
    async def delete_apsent(self, student_id: int, date: str, number: int) -> str:
        await delete_apsent(student_id=student_id, date=date, number=number)
        return '{"code": 200}'