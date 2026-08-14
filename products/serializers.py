from rest_framework import serializers
from .models import Product, Background


class ProductSerializer(serializers.ModelSerializer):
    overlay_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'overlay_image',
            'is_new',
            'gender',
            'category',
            'purchase_url',
            'like_count',
        ]

    def get_overlay_image(self, obj):
        request = self.context.get('request')
        if obj.overlay_image:
            url = obj.overlay_image.url
            return request.build_absolute_uri(url) if request else url
        return None


class BackgroundSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Background
        fields = ['id', 'name', 'image', 'type']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None