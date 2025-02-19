from django.db import migrations
from users.models.user import User

class Migration(migrations.Migration):

    def add_data(apps, schema_editor):
        user = User()

        user.username = "admin@admin.com"
        user.password = "admin"
        user.is_staff = True
        user.set_password("admin")

        user.save()

    dependencies = [
        ('users', '0004_add_initial_user_groups'),
    ]

    operations = [
        migrations.RunPython(add_data, ),
    ]
