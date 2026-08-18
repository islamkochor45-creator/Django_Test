from django.urls import reverse
from rest_framework.test import APITestCase

from apps.catalog.models import Category, Product
from apps.orders.models import Order
from apps.users.models import User


class OrderTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="user@test.com", password="TestPassword123"
        )

    def test_user_exists(self):

        self.assertEqual(User.objects.count(), 1)

    def test_customer_can_create_chat_for_order(self):
        self.client.force_authenticate(user=self.user)
        category = Category.objects.create(name="Phones", slug="phones")
        product = Product.objects.create(
            category=category,
            name="Phone",
            slug="phone",
            sku="sku-1",
            price=100,
            quantity=3,
        )
        order = Order.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            phone="123",
            address="Main",
        )
        order.items.create(product=product, quantity=1, price=product.price)

        response = self.client.post(
            "/api/orders/chat/",
            {"order_id": order.id, "message": "Hello seller"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("thread", response.data)
        self.assertEqual(response.data["message"], "Hello seller")

    def test_seller_can_update_order_status(self):
        seller = User.objects.create_user(
            email="seller@test.com",
            password="TestPassword123",
            role=User.Role.MANAGER,
        )
        order = Order.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            phone="123",
            address="Main",
        )

        self.client.force_authenticate(user=seller)
        response = self.client.patch(
            f"/api/orders/admin/status/{order.id}/",
            {"status": "processing"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "processing")
