from django.db import models


class Vertical(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "vertical"

    def __str__(self):
        return self.name
