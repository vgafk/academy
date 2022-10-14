from typing import Optional, Dict
import strawberry
from strawberry.types import Info

#
from db import models
from db.resolvers import get_group

# from db.resolvers import get_user_student_data


@strawberry.type
class Group:
    id: Optional[int]
    name: str
    full_name: Optional[str]
    faculty_id: int

    @classmethod
    def from_instance(cls, instance: models.Group) -> "Group":
        return cls(
            id=instance.id,
            name=instance.name,
            full_name=instance.full_name,
            faculty_id=instance.faculty_id
        )


@strawberry.federation.type(extend=True, keys=["id"])
class Student:
    id: strawberry.ID = strawberry.federation.field(external=True)

    @strawberry.field
    async def group(self) -> Group:
        res = await get_group(7)
        return Group.from_instance(res)
        # return Group(id=1, name='name1', faculty_id=1, full_name='full')

    @classmethod
    # def resolve_reference(cls, id: strawberry.ID) -> object:
    def resolve_reference(cls, **kwargs) -> object:
        print(kwargs)
        return Student(id=id)
