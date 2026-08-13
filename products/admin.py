from django.contrib import admin
from .models import Product, Background


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'season', 'gender', 'category', 'like_count']
    list_filter = ['season', 'gender', 'category']
    search_fields = ['name']


@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']
    list_filter = ['type']
    search_fields = ['name']