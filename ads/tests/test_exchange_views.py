from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import Category, Condition, Ad, ExchangeProposal

User = get_user_model()


class CreateExchangeViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.client.force_authenticate(user=self.user)
        self.category_obj = Category.objects.create(name="Техника")
        self.condition_obj = Condition.objects.create(name="Б/у")
        self.test_ad_obj1 = Ad.objects.create(user=self.user, title="Телефон", description="Хороший телефон",
                                             category=self.category_obj, condition=self.condition_obj)

        self.test_ad_obj2 = Ad.objects.create(user=self.user, title="MP3 плеер", description="Хороший плеер",
                                             category=self.category_obj, condition=self.condition_obj)

    def test_correct_data(self):
        data = {
            "ad_sender_id": self.test_ad_obj1.id,
            "ad_receiver_id": self.test_ad_obj2.id,
            "comment": "Давай меняться?"
        }

        response = self.client.post(reverse('create-exchange'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_created'], True)

    def test_correct_data_no_comment(self):
        data = {
            "ad_sender_id": self.test_ad_obj1.id,
            "ad_receiver_id": self.test_ad_obj2.id,
        }

        response = self.client.post(reverse('create-exchange'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_created'], True)

    def test_incorrect_fields(self):
        data = {
            "ad_sender_id": self.test_ad_obj1.id,
            "comment": "Давай меняться?"
        }

        response = self.client.post(reverse('create-exchange'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_created'], False)

    def test_incorrect_ids(self):
        data = {
            "ad_sender_id": 5252,
            "ad_receiver_id": 2525,
            "comment": "Давай меняться?"
        }

        response = self.client.post(reverse('create-exchange'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_created'], False)

    def test_equal_ids(self):
        data = {
            "ad_sender_id": self.test_ad_obj1.id,
            "ad_receiver_id": self.test_ad_obj1.id,
            "comment": "Давай меняться?"
        }

        response = self.client.post(reverse('create-exchange'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_created'], False)


class EditExchangeViewText(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.user_second = User.objects.create_user(
            username='seconduser',
            password='secondpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.client_second = APIClient()
        self.client_second.force_authenticate(user=self.user_second)

        self.client.force_authenticate(user=self.user)
        self.category_obj = Category.objects.create(name="Техника")
        self.condition_obj = Condition.objects.create(name="Б/у")
        self.test_ad_obj1 = Ad.objects.create(user=self.user, title="Телефон", description="Хороший телефон",
                                             category=self.category_obj, condition=self.condition_obj)
        self.test_ad_obj2 = Ad.objects.create(user=self.user, title="MP3 плеер", description="Хороший плеер",
                                              category=self.category_obj, condition=self.condition_obj)
        self.test_exchange_obj = ExchangeProposal.objects.create(ad_sender=self.test_ad_obj1,
                                                                 ad_receiver=self.test_ad_obj2)

    def test_correct_data_accepted(self):
        data = {
            "exchange_id": self.test_exchange_obj.id,
            "status": "accepted"
        }

        response = self.client.post(reverse('edit-exchange'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_edited'], True)

    def test_correct_data_declined(self):
        data = {
            "exchange_id": self.test_exchange_obj.id,
            "status": "declined"
        }

        response = self.client.post(reverse('edit-exchange'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_edited'], True)

    def test_incorrect_id(self):
        data = {
            "exchange_id": 5252,
            "status": "declined"
        }

        response = self.client.post(reverse('edit-exchange'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_edited'], False)

    def test_incorrect_user(self):
        data = {
            "exchange_id": self.test_exchange_obj.id,
            "status": "accepted"
        }

        response = self.client_second.post(reverse('edit-exchange'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_edited'], False)


class ExchangesViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.category_obj = Category.objects.create(name="Техника")
        self.condition_obj = Condition.objects.create(name="Б/у")
        self.test_ad_obj1 = Ad.objects.create(user=self.user, title="Телефон", description="Хороший телефон",
                                              category=self.category_obj, condition=self.condition_obj)
        self.test_ad_obj2 = Ad.objects.create(user=self.user, title="MP3 плеер", description="Хороший плеер",
                                              category=self.category_obj, condition=self.condition_obj)
        self.test_exchange_obj = ExchangeProposal.objects.create(ad_sender=self.test_ad_obj1,
                                                                 ad_receiver=self.test_ad_obj2)

    def test_no_filters(self):
        data = {
        }

        response = self.client.post(reverse('exchanges'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_by_sender(self):
        data = {
            "sender_username": "testuser"
        }

        response = self.client.post(reverse('exchanges'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_by_incorrect_sender(self):
        data = {
            "sender_username": "incorrectuser"
        }

        response = self.client.post(reverse('exchanges'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_by_receiver(self):
        data = {
            "receiver_username": "testuser"
        }

        response = self.client.post(reverse('exchanges'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_by_incorrect_receiver(self):
        data = {
            "receiver_username": "incorrectuser"
        }

        response = self.client.post(reverse('exchanges'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_by_status_accepted(self):
        data = {
            "status": "accepted"
        }

        response = self.client.post(reverse('exchanges'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_by_status_pending(self):
        data = {
            "status": "pending"
        }

        response = self.client.post(reverse('exchanges'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_by_status_declined(self):
        data = {
            "status": "declined"
        }

        response = self.client.post(reverse('exchanges'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_by_incorrect_status(self):
        data = {
            "status": "fakestatus"
        }

        response = self.client.post(reverse('exchanges'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
