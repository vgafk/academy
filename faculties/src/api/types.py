from typing import Optional, Dict
import strawberry

from db import models
from db.resolvers import get_group, get_faculty


@strawberry.federation.type
class Faculty:
    id: strawberry.ID
    name: str

    @classmethod
    def from_instance(cls, instance: models.Faculty) -> "Faculty":
        return cls(
            id=strawberry.ID(str(instance.id)),
            name=instance.name
        )


@strawberry.federation.type(extend=True, keys=["id"])
class Group:
    id: strawberry.ID = strawberry.federation.field(external=True)
    name: Optional[str]
    full_name: Optional[str]
    faculty_id: Optional[int]

    @strawberry.field
    async def faculty(self) -> Faculty:
        res = await get_faculty(faculty_id=self.faculty_id)
        return Faculty.from_instance(res)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID) -> object:
        res = await get_group(group_id=int(id))
        return Group.from_instance(res)

    @classmethod
    def from_instance(cls, instance: models.Group) -> "Group":
        return cls(
            id=strawberry.ID(str(instance.id)),
            name=instance.name,
            full_name=instance.full_name,
            faculty_id=instance.faculty_id
        )