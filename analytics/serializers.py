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


class ProductLikeCountSerializer(serializers.ModelSerializer): # 상품 별 구매 링크 클릭 횟수
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

class ProductSessionSerializer(serializers.ModelSerializer):
    session_count = serializers.IntegerField(
        source='choose_count',
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'color',
            'size',
            'is_new',
            'session_count',
        ]

class TotalLinkAnalyticsSerializer(serializers.Serializer): # 전체 링크 받기 횟수, 전체 링크 클릭 횟수
    total_link_received = serializers.IntegerField()
    total_link_click = serializers.IntegerField()

class TodayLikeCountSerializer(serializers.Serializer): # 구매 링크 클릭 횟수(하루)
    today_click_count = serializers.IntegerField()

class TodayLinkCountSerializer(serializers.Serializer): # 링크 받기 한 수(하루)
    today_link_count = serializers.IntegerField()

class TodayVisitorCountSerializer(serializers.Serializer):
    today_visitor_count = serializers.IntegerField()