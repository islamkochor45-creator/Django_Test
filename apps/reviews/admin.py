from django.contrib import admin
from .models import Review


# Register your models here.
@admin.register(Review)
class ResviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "rating",
        "text",
        "created_at",
        "updated_at",
    )
