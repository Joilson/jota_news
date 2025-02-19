from django.contrib.auth.models import Group

from users.models.user import User
from users.models.user import UserType
from users.repositories.user import UserRepository


class UserService:
    @staticmethod
    def list():
        return UserRepository.get_all()

    @staticmethod
    def get(product_id):
        return UserRepository.get_by_id(product_id)

    @staticmethod
    def create(data) -> User:
        if data['type'] == UserType.ADMIN:
            data['is_staff'] = True

        user = UserRepository.create(data)
        UserService.relate_user_and_permissions(user, data['type'])

        return user

    @staticmethod
    def update(user, data) -> User:
        return UserRepository.update(user, data)

    @staticmethod
    def delete(product_id):
        return UserRepository.delete(product_id)

    @staticmethod
    def relate_user_and_permissions(user: User, received_type: str):
        if UserType.ADMIN.value in received_type: # type: ignore
            return

        group_name = None
        if UserType.EDITOR.value in received_type: # type: ignore
            group_name = UserType.EDITOR.value # type: ignore
        if UserType.READER.value in received_type: # type: ignore
            group_name = UserType.READER.value # type: ignore

        if group_name is None:
            raise ValueError('Tipo de usuário inválido')

        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist as ex:
            raise ValueError(f"O grupo '{group_name}' não existe.") from ex
