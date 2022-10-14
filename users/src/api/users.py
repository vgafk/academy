import strawberry
from db import models


@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID
    login: str

    @classmethod
    def from_instance(cls, instance: models.User) -> "User":
        return cls(
            id=instance.id,
            login=instance.login
        )


@strawberry.type
class UserNotFound:
    message: str = "Пользователя с представленным id не существует"


@strawberry.type
class UserLoginExists:
    message: str = "Пользователь с таким логином уже существует"


@strawberry.type
class UserAddSucces:
    message: str = "Пользователь успешно добавлен"


SelectUserResponse = strawberry.union("SelectUserResponse",
                                      (User,
                                       UserNotFound))

UserAddResponse = strawberry.union("UserAddResponse",
                                   (UserAddSucces,
                                    UserLoginExists))