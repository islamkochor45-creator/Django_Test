from django.db import models

from apps.orders.models import Order


class Payment(models.Model):

    PAYMENT_STATUS = (
        ("pending", "Ожидание"),
        ("paid", "Оплачено"),
        ("failed", "Ошибка"),
        ("cancelled", "Отменено"),
    )

    PAYMENT_METHODS = (
        ("card", "Банковская карта"),
        ("cash", "Наличные"),
    )

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="card")

    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")

    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"Payment #{self.id}"
