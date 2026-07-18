from rest_framework.test import APITestCase

from apps.users.models import User


class OrderTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="user@test.com", password="TestPassword123"
        )

    def test_user_exists(self):

        self.assertEqual(User.objects.count(), 1)
