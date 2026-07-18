from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Category
from apps.catalog.models import Product


class ProductTest(APITestCase):

    def setUp(self):

        category = Category.objects.create(name="Телефоны", slug="phones")

        Product.objects.create(
            category=category,
            name="Samsung A25",
            slug="samsung-a25",
            sku="A25",
            price=10000,
            quantity=5,
        )

    def test_products(self):

        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
