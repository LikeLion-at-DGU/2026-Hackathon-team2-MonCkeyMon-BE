from rest_framework import serializers
from products.models import Product, Background


class ProductChooseCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'choose_count',
        ]


class BackgroundChooseCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = [
            'id',
            'name',
            'choose_count',
        ]


class ProductLikeCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'like_count',
        ]


class CompletedExperienceCountSerializer(serializers.Serializer):
    completed_experience_count = serializers.IntegerField()