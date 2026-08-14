from django.contrib import admin
from .models import Product, Background


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'category', 'is_new', 'like_count']
    list_filter = ['gender', 'category', 'is_new']
    search_fields = ['name']


@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']
    list_filter = ['type']
    search_fields = ['name']