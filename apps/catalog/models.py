from django.db import models
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")

    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")

    description = models.TextField(blank=True, verbose_name="Описание")

    image = models.ImageField(
        upload_to="categories/", blank=True, null=True, verbose_name="Изображение"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активна")

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):

    class Status(models.TextChoices):
        AVAILABLE = "available", "В наличии"
        OUT_OF_STOCK = "out", "Нет в наличии"
        DISCONTINUED = "discontinued", "Снят с продажи"

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    name = models.CharField(max_length=200)

    slug = models.SlugField(max_length=200, unique=True)

    description = models.TextField(blank=True)

    sku = models.CharField(max_length=100, unique=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField(default=0)

    brand = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )

    image = models.ImageField(upload_to="products/")

    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def __str__(self):
        return f"Image for {self.product.name}"


@property
def average_rating(self):

    result = self.reviews.aggregate(avg=Avg("rating"))

    return result["avg"] or 0
