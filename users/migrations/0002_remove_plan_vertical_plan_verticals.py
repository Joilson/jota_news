# Generated by Django 5.1.6 on 2025-02-19 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial_user_tables'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='vertical',
        ),
        migrations.AddField(
            model_name='plan',
            name='verticals',
            field=models.ManyToManyField(related_name='plans', to='users.vertical'),
        ),
    ]
