from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class UserRegistrationTest(APITestCase):

    def test_user_registration(self):

        url = "/api/auth/register/"

        data = {
            "email": "test@example.com",
            "password": "TestPassword123",
            "first_name": "Ivan",
            "last_name": "Ivanov",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 1)

        self.assertEqual(User.objects.first().email, "test@example.com")


class JWTTokenTest(APITestCase):

    def setUp(self):

        User.objects.create_user(email="test@example.com", password="TestPassword123")

    def test_get_token(self):

        response = self.client.post(
            "/api/token/", {"email": "test@example.com", "password": "TestPassword123"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access", response.data)

        self.assertIn("refresh", response.data)
