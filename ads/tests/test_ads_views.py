from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import Category, Condition, Ad

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

    # Все данные корректны
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

    # Не все поля переданы
    def test_incorrect_fields(self):
        data = {
            "title": "Телефон",
            "description": "Хороший телефон",
        }

        response = self.client.post(reverse('create-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_created'], False)

    # Не корректная категория
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

    # Не корректное состояние
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


class DeleteAdViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category_obj = Category.objects.create(name="Техника")
        self.condition_obj = Condition.objects.create(name="Б/у")
        self.test_ad_obj = Ad.objects.create(user=self.user, title="Телефон", description="Хороший телефон",
                                             category=self.category_obj, condition=self.condition_obj)

    # Все данные корректны
    def test_correct_data(self):
        data = {
            "ad_id": self.test_ad_obj.id
        }

        response = self.client.post(reverse('delete-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_deleted'], True)

    # Не все поля переданы
    def test_incorrect_fields(self):
        data = {}

        response = self.client.post(reverse('delete-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_deleted'], False)

    # Не корректный id объявления
    def test_incorrect_ad_id(self):
        data = {
            "ad_id": 5252
        }

        response = self.client.post(reverse('delete-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_deleted'], False)


class EditAdViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category_obj = Category.objects.create(name="Техника")
        Category.objects.create(name="Часы")
        self.condition_obj = Condition.objects.create(name="Б/у")
        Condition.objects.create(name="Новое")
        self.test_ad_obj = Ad.objects.create(user=self.user, title="Телефон", description="Хороший телефон",
                                             category=self.category_obj, condition=self.condition_obj)

    # Все данные корректны
    def test_correct_data(self):
        data = {
            "ad_id": self.test_ad_obj.id,
            "title": "Часы Casio Vintage",
            "description": "Крутые часы",
            "category": "Часы",
            "condition": "Новое"
        }

        response = self.client.post(reverse('edit-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_edited'], True)

    # Не корректный id объявления
    def test_incorrect_ad_id(self):
        data = {
            "ad_id": 5252,
            "title": "Часы Casio Vintage",
            "description": "Крутые часы",
            "category": "Часы",
            "condition": "Новое"
        }

        response = self.client.post(reverse('edit-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_edited'], False)

    # Не все поля переданы
    def test_incorrect_fields(self):
        data = {
            "ad_id": self.test_ad_obj.id,
            "title": "Часы Casio Vintage"
        }

        response = self.client.post(reverse('edit-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_edited'], False)

    # Не корректная категория
    def test_incorrect_category(self):
        data = {
            "ad_id": self.test_ad_obj.id,
            "title": "Телефон",
            "description": "Хороший телефон",
            "category": "OGREMAGI",
            "condition": "Новое"
        }

        response = self.client.post(reverse('edit-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_edited'], False)

    # Не корректное состояния
    def test_incorrect_condition(self):
        data = {
            "ad_id": self.test_ad_obj.id,
            "title": "Телефон",
            "description": "Хороший телефон",
            "category": "Техника",
            "condition": "MULTICAST"
        }

        response = self.client.post(reverse('edit-ad'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_edited'], False)


class AdsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.category_obj = Category.objects.create(name="Техника")
        self.condition_obj = Condition.objects.create(name="Б/у")
        self.test_ad_obj1 = Ad.objects.create(user=self.user, title="Телефон", description="Хороший телефон",
                                              category=self.category_obj, condition=self.condition_obj)
        self.test_ad_obj2 = Ad.objects.create(user=self.user, title="MP3 плеер", description="Хороший плеер",
                                              category=self.category_obj, condition=self.condition_obj)

    def test_no_filters(self):
        data = {
        }

        response = self.client.post(reverse('ads'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_query(self):
        data = {
            "query": "тел"
        }

        response = self.client.post(reverse('ads'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_fake_query(self):
        data = {
            "query": "еда"
        }

        response = self.client.post(reverse('ads'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_by_category(self):
        data = {
            "category": "Техника"
        }

        response = self.client.post(reverse('ads'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_by_incorrect_category(self):
        data = {
            "category": "fakecategory"
        }

        response = self.client.post(reverse('ads'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_by_condition(self):
        data = {
            "condition": "Б/у"
        }

        response = self.client.post(reverse('ads'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_by_incorrect_condition(self):
        data = {
            "condition": "fakecondition"
        }

        response = self.client.post(reverse('ads'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
