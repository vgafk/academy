from typing import Optional, List

import strawberry

from api.types import SelectStudentResponse, StudentNotFound, Student
from db.resolvers import get_student_data, get_students, get_group_students


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