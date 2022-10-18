from typing import Optional, List

import strawberry
from strawberry.file_uploads import Upload

from api.types import Group, Faculty
from db.resolvers import get_groups, get_group, get_groups_by_faculty, get_faculties, get_faculty
from files.files_handel import FileHandler


@strawberry.type
class Query:

    @strawberry.federation.field
    async def groups(self) -> List[Group]:
        res = await get_groups()
        return [Group.from_instance(group) for group in res]

    @strawberry.field
    async def group(self, group_id: int) -> Group:
        res = await get_group(group_id=group_id)
        return Group.from_instance(res)

    @strawberry.field
    async def faculty_groups(self, faculty_id: int) -> List[Group]:
        res = await get_groups_by_faculty(faculty_id=faculty_id)
        return [Group.from_instance(group) for group in res]

    @strawberry.federation.field
    async def faculties(self) -> List[Faculty]:
        res = await get_faculties()
        return [Faculty.from_instance(faculty) for faculty in res]

    @strawberry.field
    async def faculty(self, faculty_id: int) -> Faculty:
        res = await get_faculty(faculty_id=faculty_id)
        return Faculty.from_instance(res)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def upload_groups(self, file: Upload) -> str:
        await FileHandler.add_batch_group(data_bytes=await file.read())
        return '{"code": 200}'
