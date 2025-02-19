from rest_framework.permissions import BasePermission

from users.models.user import UserType


class IsEditorUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=UserType.EDITOR.value).exists()


class IsReaderUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=UserType.READER.value).exists()
