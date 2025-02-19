from news.repositories.news import NewsRepository
from news.services.files import NewsImage
from users.models.user import User


class NewsService:
    @staticmethod
    def list():
        return NewsRepository.get_all()

    @staticmethod
    def get(entity_id):
        return NewsRepository.get_by_id(entity_id)

    @staticmethod
    def create(data):
        image_path = NewsImage().upload(data['image'])
        data['image'] = image_path

        return NewsRepository.create(data)

    @staticmethod
    def delete(instance):
        return NewsRepository.delete(instance.id)

    @staticmethod
    def update(entity, data):
        return NewsRepository.update(entity, data)

    @staticmethod
    def find_for_readers(user: User):
        verticals = user.plan.verticals.all()
        return NewsRepository.find_published_for_verticals(verticals)
