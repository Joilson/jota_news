from django.db import migrations

from users.models.permissions import ReaderPermissions
from users.models.user import UserType


class Migration(migrations.Migration):

    def add_groups(apps, schema_editor):
        group = apps.get_model("auth", "Group")
        Permission = apps.get_model("auth", "Permission")

        permission_codes_editor = [
            ReaderPermissions.NEWS_ADD.value,
            ReaderPermissions.NEWS_VIEW.value,
            ReaderPermissions.NEWS_CHANGE.value,
            ReaderPermissions.NEWS_DELETE.value
        ]
        permission_codes_reader = [ReaderPermissions.NEWS_VIEW.value]

        editor, _ = group.objects.get_or_create(name=UserType.EDITOR.value)
        reader, _ = group.objects.get_or_create(name=UserType.READER.value)

        editor_permissions = Permission.objects.filter(codename__in=permission_codes_editor)
        reader_permissions = Permission.objects.filter(codename__in=permission_codes_reader)

        editor.permissions.add(*editor_permissions)
        reader.permissions.add(*reader_permissions)

    def rm_groups(apps, schema_editor):
        Group = apps.get_model("auth", "Group")
        Group.objects.filter(name__in=[UserType.EDITOR.value, UserType.READER.value]).delete()

    dependencies = [
        ('users', '0003_initial_plans_and_verticals'),
    ]

    operations = [
        migrations.RunPython(add_groups, rm_groups),
    ]
