from typing import Optional, List

import strawberry

from api.types import User, SelectUserResponse, UserAddResponse, UserAddSucces, UserLoginExists, InDevelopment
from db.resolvers import get_users, get_user, add_user


@strawberry.type
class Query:

    @strawberry.field
    async def users(self) -> List[User]:
        users = await get_users()
        return [User.from_instance(user) for user in users]

    @strawberry.field
    async def user(self, user_id: Optional[int] = None, login: Optional[str] = None) -> SelectUserResponse:
        users = await get_user(user_id=user_id, login=login)
        return User.from_instance(users)


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def add_user(self, login: str, password: str) -> UserAddResponse:
        res = await add_user(login, password)
        if res:
            return UserAddSucces
        else:
            return UserLoginExists

    @strawberry.mutation
    async def change_password(self, user_id: int, password: str) -> InDevelopment:
        return InDevelopment

    @strawberry.mutation
    async def delete_user(self, user_id: int) -> InDevelopment:
        return InDevelopment
