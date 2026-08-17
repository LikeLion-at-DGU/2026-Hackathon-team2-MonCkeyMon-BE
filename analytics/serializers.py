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


class TotalVisitorCountSerializer(serializers.Serializer):
    total_visitor_count = serializers.IntegerField()


class DailyVisitorCountSerializer(serializers.Serializer):
    date = serializers.DateField()
    count = serializers.IntegerField()

class ProductInterestSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()

    color = serializers.CharField()
    size = serializers.CharField()
    gender = serializers.CharField()
    category = serializers.CharField()

    session_count = serializers.IntegerField()
    link_received_count = serializers.IntegerField()
    link_click_count = serializers.IntegerField()
    total_score = serializers.IntegerField()

class CategorySessionTopSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    category = serializers.CharField()
    session_count = serializers.IntegerField()