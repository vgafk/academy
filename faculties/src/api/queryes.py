from typing import Optional, List

import strawberry

from api.types import Group
from db.resolvers import get_groups, get_group


@strawberry.type
class Query:

    @strawberry.field
    async def groups(self) -> List[Group]:
        res = await get_groups()
        return [Group.from_instance(group) for group in res]

    @strawberry.field
    async def group(self, group_id: int) -> Group:
        res = await get_group(group_id=group_id)
        return Group.from_instance(res)


        # res = await get_student_data(student_id)
        # if not res:
        #     return StudentNotFound
        # else:
        #     return Student.marshal(res)
