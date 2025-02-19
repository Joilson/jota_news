from django.db import models

from news.services.files import NewsImage
from users.models.user import User
from users.models.vertical import Vertical


class NewsStatus(models.TextChoices):
    DRAFT = 'draft', 'Rascunho'  # ainda em preenchimento, incompleta
    PUBLICATION = 'publication', 'Publicação'  # ok para publicação


class NewsVisibility(models.TextChoices):
    PUBLIC = 'public', 'Publica'  # Visivel para todos os publicos
    PRO = 'pro', 'Pró'  # visivel apenas para usuários pró


class News(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    image = models.ImageField(upload_to=NewsImage.PATH)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    scheduled_to = models.DateTimeField(auto_now_add=False, null=True)
    status = models.CharField(max_length=20, choices=NewsStatus.choices)
    visibility = models.CharField(max_length=20, choices=NewsVisibility.choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    verticals = models.ManyToManyField(Vertical, related_name="verticals")

    class Meta:
        db_table = "news"
