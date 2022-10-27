import datetime
from typing import Optional, List
import strawberry

from db import models
from db.resolvers import get_user_student_data, get_student_data, get_absents


@strawberry.federation.type(keys=["id"])
class Group:
    id: strawberry.ID


@strawberry.federation.type(keys=["id"])
class Student:
    id: strawberry.ID
    user_id: int
    surname: str
    name: str
    middle_name: Optional[str]
    snils: Optional[str]
    inn: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    group_id: int

    @strawberry.field
    async def group(self, root: 'Student') -> Group:
        return Group(id=root.group_id)

    @strawberry.field
    async def absents(self) -> List["Absent"]:
        res = await get_absents(int(self.id))
        return [Absent.from_instance(absent) for absent in res]


    @classmethod
    def from_instance(cls, instance: models.Student) -> "Student":
        return cls(
            id=strawberry.ID(str(instance.id)),
            user_id=instance.user_id,
            surname=instance.surname,
            name=instance.name,
            middle_name=instance.middle_name,
            snils=instance.snils,
            inn=instance.inn,
            email=instance.email,
            phone=instance.phone,
            group_id=instance.group_id
        )

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID) -> "Student":
        res = await get_student_data(int(id))
        return Student.from_instance(res)


@strawberry.type
class StudentNotFound:
    error: str = "Couldn't find an student with the supplied id"


SelectStudentResponse = strawberry.union("SelectStudentResponse",
                                         (Student,
                                          StudentNotFound))


@strawberry.federation.type(extend=True, keys=["id"])
class User:
    id: strawberry.ID = strawberry.federation.field(external=True)

    @strawberry.field
    async def student(self) -> SelectStudentResponse:
        res = await get_user_student_data(int(self.id))
        if not res:
            return StudentNotFound

        return Student.from_instance(res)

    @classmethod
    def resolve_reference(cls, id: strawberry.ID) -> object:
        return User(id=id)


@strawberry.type
class Absent:
    id: strawberry.ID
    student_id: int
    date: datetime.date
    number: int

    @classmethod
    def from_instance(cls, instance: models.Absents) -> "Absent":
        return cls(
            id=strawberry.ID(str(instance.id)),
            student_id=instance.student_id,
            date=instance.date,
            number=instance.number
        )
