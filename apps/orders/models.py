from django.conf import settings
from django.db import models

from apps.catalog.models import Product


class Order(models.Model):

    STATUS_CHOICES = (
        ("new", "Новый"),
        ("processing", "В обработке"),
        ("shipped", "Отправлен"),
        ("completed", "Завершен"),
        ("cancelled", "Отменен"),
    )
    PAYMENT_CHOICES = (
        ("unpaid", "Не оплачено"),
        ("paid", "Оплачено"),
        ("refunded", "Возвращено"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=30)

    address = models.TextField()

    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default="unpaid"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"Order #{self.id}"

    @property
    def total_price(self):

        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):

        return self.price * self.quantity

    def __str__(self):

        return self.product.name
