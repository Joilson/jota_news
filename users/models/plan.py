from django.db import models

from users.models.vertical import Vertical


class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(null=False)
    verticals = models.ManyToManyField(Vertical, related_name="plans")

    class Meta:
        db_table = "plans"

    def __str__(self):
        return self.name
