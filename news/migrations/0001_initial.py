# Generated by Django 5.1.6 on 2025-02-19 12:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0005_add_admin_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='uploads/news/')),
                ('content', models.TextField()),
                ('published_at', models.DateTimeField(auto_now_add=True)),
                ('scheduled_to', models.DateTimeField(auto_now_add=False, null=True)),
                ('status', models.CharField(choices=[('draft', 'Rascunho'), ('publication', 'Publicação')], max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('verticals', models.ManyToManyField(related_name='verticals', to='users.vertical')),
            ],
            options={
                'db_table': 'news',
            },
        ),
    ]
