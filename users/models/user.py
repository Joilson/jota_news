from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models.plan import Plan


class UserType(models.TextChoices):
    EDITOR = 'editor', 'Editor'
    READER = 'reader', 'Leitor'
    ADMIN = 'admin', 'Admin'


class User(AbstractUser):
    type = models.CharField(max_length=10, choices=UserType.choices)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = "users"
