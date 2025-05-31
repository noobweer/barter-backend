from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import Category, Condition

User = get_user_model()


class CreateAdViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        Category.objects.create(name="Техника")
        Category.objects.create(name="Часы")
        Condition.objects.create(name="Новое")
        Condition.objects.create(name="Б/у")

    def test_correct_data(self):
        data = {
            "title": "Телефон",
            "description": "Хороший телефон",
            "category": "Часы",
            "condition": "Новое"
        }

        response = self.client.post(reverse('create-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_created'], True)

    def test_incorrect_fields(self):
        data = {
            "title": "Телефон",
            "description": "Хороший телефон",
        }

        response = self.client.post(reverse('create-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_created'], False)

    def test_incorrect_category(self):
        data = {
            "title": "Телефон",
            "description": "Хороший телефон",
            "category": "OGREMAGI",
            "condition": "Новое"
        }

        response = self.client.post(reverse('create-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_created'], False)

    def test_incorrect_condition(self):
        data = {
            "title": "Телефон",
            "description": "Хороший телефон",
            "category": "Техника",
            "condition": "MULTICAST"
        }

        response = self.client.post(reverse('create-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_created'], False)
