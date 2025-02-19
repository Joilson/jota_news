import uuid

from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserViewSetTests(APITestCase):
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

        self.admin_token = RefreshToken.for_user(self.admin_user).access_token
        self.editor_token = RefreshToken.for_user(self.editor_user).access_token
        self.reader_token = RefreshToken.for_user(self.reader_user).access_token

        self.user_data = {
            "password": "test",
            "username": f"user_{uuid.uuid4().hex[:8]}@test.com",
            "type": "reader",
            "plan": 1
        }

    def test_list_users_as_admin(self):
        url = '/api/users/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_list_users_as_editor_user(self):
        url = '/api/users/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.editor_token}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_as_reader_user(self):
        url = '/api/users/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reader_token}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user(self):
        url = f'/api/users/{self.reader_user.id}/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.reader_user.username)

    def test_retrieve_user_not_found(self):
        url = '/api/users/9999/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        url = '/api/users/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_create_user_unauthorized_by_auditor(self):
        url = '/api/users/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.editor_token}')
        response = self.client.post(url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_unauthorized_by_reader(self):
        url = '/api/users/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reader_token}')
        response = self.client.post(url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user(self):
        url = f'/api/users/{self.reader_user.id}/'
        updated_data = {'username': 'updated@example.com', 'password': "xxx", 'type': 'admin'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], updated_data['username'])

    def test_update_user_not_found(self):
        url = '/api/users/9999/'
        updated_data = {'username': 'updateduser'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        url = f'/api/users/{self.reader_user.id}/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
