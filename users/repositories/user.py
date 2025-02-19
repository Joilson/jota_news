from typing import cast

from users.models.user import User


class UserRepository:
    @staticmethod
    def get_all() -> list[User]:
        return User.objects.all()

    @staticmethod
    def get_by_id(product_id) -> User | None:
        return User.objects.filter(id=product_id).first()

    @staticmethod
    def create(data) -> User:
        return User.objects.create_user(**data)

    @staticmethod
    def update(user, data) -> User:
        if "password" in data:
            user.set_password(data.pop("password"))
            user.save(update_fields=["password"])

        User.objects.filter(id=user.id).update(**data)

        return cast(User, UserRepository.get_by_id(user.id))

    @staticmethod
    def delete(product_id) -> bool:
        return User.objects.filter(id=product_id).delete()
