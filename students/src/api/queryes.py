from typing import Optional, List

import strawberry
from strawberry.file_uploads import Upload

from api.types import SelectStudentResponse, StudentNotFound, Student
from db.resolvers import get_student_data, get_students, get_group_students
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