from django.contrib import admin

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "slug",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "slug",
    )

    list_filter = ("is_active",)

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "quantity",
        "status",
        "is_active",
    )

    list_filter = (
        "category",
        "status",
        "is_active",
        "brand",
    )

    search_fields = (
        "name",
        "sku",
        "brand",
    )

    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "is_main",
        "created_at",
    )

    list_filter = ("is_main",)
