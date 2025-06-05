from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import Category, Condition, Ad, ExchangeProposal

User = get_user_model()


class UserInfoViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_userinfo(self):
        response = self.client.get(reverse('user-info'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['account'], self.user.username)


class CategoriesViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        Category.objects.create(name='Техника')
        Category.objects.create(name='Часы')
        Category.objects.create(name='Одежда')
        Category.objects.create(name='Запчасти')

    def test_categories(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


class ConditionsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        Condition.objects.create(name='Б/у')
        Condition.objects.create(name='Новое')

    def test_categories(self):
        response = self.client.get(reverse('conditions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
