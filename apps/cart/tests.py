from rest_framework.test import APITestCase

from apps.users.models import User
from apps.catalog.models import Category
from apps.catalog.models import Product


class CartTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="test@example.com", password="TestPassword123"
        )

        response = self.client.post(
            "/api/token/", {"email": "test@example.com", "password": "TestPassword123"}
        )

        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        category = Category.objects.create(name="Телефоны", slug="phones")

        self.product = Product.objects.create(
            category=category,
            name="Samsung",
            slug="samsung",
            sku="S001",
            price=10000,
            quantity=10,
        )

    def test_add_to_cart(self):

        response = self.client.post(
            "/api/cart/add/", {"product_id": self.product.id, "quantity": 2}
        )

        self.assertEqual(response.status_code, 200)
