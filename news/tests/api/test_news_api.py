import io
from datetime import datetime, timedelta

from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.test import APITestCase

from news.models.news import News

User = get_user_model()


class NewsViewSetTests(APITestCase):

    def generate_image(self):
        img_io = io.BytesIO()
        image = Image.new("RGB", (100, 100), color=(255, 0, 0))
        image.save(img_io, format="JPEG")
        img_io.seek(0)
        return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")

    def setUp(self):
        editor_group = Group.objects.get(name='editor')
        reader_group = Group.objects.get(name='reader')

        self.admin_user = User.objects.create_user(
            username='admin', email='admin@example.com', password='xxx', is_staff=True
        )

        self.editor_user = User.objects.create_user(
            username='editor', email='editor@example.com', password='xxx'
        )
        self.editor_user.groups.add(editor_group)

        self.reader_user = User.objects.create_user(
            username='reader', email='reader@example.com', password='xxx'
        )
        self.reader_user.groups.add(reader_group)

        self.news = News.objects.create(
            title="Notícia Teste",
            content="Conteúdo da notícia",
            author=self.editor_user,
            image=self.generate_image()
        )

        self.client.force_authenticate(user=self.editor_user)
        self.url = "/api/news/"

    def test_list_news(self):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve_news(self):
        response = self.client.get(f"{self.url}{self.news.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == self.news.title

    def test_create_news(self):
        data = {
            "title": "New",
            "subtitle": "news",
            "content": "asdasdasd",
            "status": "publication",
            "visibility": "public",
            "verticals": 1,
            "image": self.generate_image()
        }

        response = self.client.post(f"{self.url}", data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New"

    def test_update_news(self):
        updated_data = {
            "title": "First",
            "subtitle": "news",
            "content": "asdasdasd",
            "status": "publication",
            "visibility": "public",
            "verticals": 1,
            "image": self.generate_image()
        }

        response = self.client.put(
            f"{self.url}{self.news.id}/",
            updated_data,
            format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "First"
        assert response.data["subtitle"] == "news"
        assert response.data["status"] == "publication"
        assert response.data["visibility"] == "public"

    def test_schedule_news(self):
        new_scheduled_date = make_aware(datetime.now() + timedelta(days=5))
        response = self.client.patch(
            f"{self.url}{self.news.id}/",
            {"scheduled_to": new_scheduled_date},
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

    def test_delete_news(self):
        response = self.client.delete(f"{self.url}{self.news.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert News.objects.count() == 0

    def test_reader_cannot_create_news(self):
        self.client.force_authenticate(user=self.reader_user)
        new_data = {
            "title": "Notícia Inválida",
            "content": "Leitor não pode criar",
            "author": self.reader_user.id,
            "scheduled_to": make_aware(datetime.now() + timedelta(days=2))
        }
        response = self.client.post(self.url, new_data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
