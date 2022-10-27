from typing import Optional

import strawberry
from db import models


@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID
    login: str
    password: Optional[str]

    @classmethod
    def from_instance(cls, instance: models.User) -> "User":
        return cls(
            id=strawberry.ID(str(instance.id)),
            login=instance.login,
            password=instance.password
        )


@strawberry.type
class UserNotFound:
    error: str = "Пользователя с представленным id не существует"


@strawberry.type
class UserLoginExists:
    error: str = "Пользователя с таким логином уже существует"


@strawberry.type
class UserAddSucces:
    message: str = "Пользователь успешно добавлен"


SelectUserResponse = strawberry.union("SelectUserResponse",
                                      (User,
                                       UserNotFound))

UserAddResponse = strawberry.union("UserAddResponse",
                                   (UserAddSucces,
                                    UserLoginExists,
                                    ))


@strawberry.type
class InDevelopment:
    error: str = 'Функция в разработке'
