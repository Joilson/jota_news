from django.db.models import Q
from django.utils.timezone import now

from news.models.news import News


class NewsRepository:
    @staticmethod
    def get_all():
        return News.objects.all()

    @staticmethod
    def get_by_id(product_id):
        return News.objects.filter(id=product_id).first()

    @staticmethod
    def create(data):
        verticals = data.pop("verticals", [])

        news = News.objects.create(**data)
        news.verticals.set(verticals)

        return news

    @staticmethod
    def delete(product_id):
        return News.objects.filter(id=product_id).delete()

    @staticmethod
    def update(entity: News, data: dict) -> News:
        verticals = data.pop("verticals", [])
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        entity.verticals.set(verticals)
        entity.save()
        
        return entity

    @staticmethod
    def find_published_for_verticals(verticals):
        news = News.objects.filter(
            Q(verticals__in=verticals) | Q(verticals__isnull=True),
            status="publication"
        ).filter(
            Q(scheduled_to__isnull=True) | Q(scheduled_to__gt=now())
        ).distinct()

        return news
