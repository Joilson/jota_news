from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict

from .models.news import News
from .publishers.async_events import send_to_other_projects


@receiver(post_save, sender=News)
def news_was_created(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    body = model_to_dict(instance)
    body["image"] = instance.image.url if instance.image else None

    if isinstance(body["scheduled_to"], datetime):
        body["scheduled_to"] = body["scheduled_to"].isoformat()

    body['verticals'] = [
        {"id": v.id, "name": v.name} for v in instance.verticals.all()
    ]

    send_to_other_projects({"type": "news.created", 'body': body})
