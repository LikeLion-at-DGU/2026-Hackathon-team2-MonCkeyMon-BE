from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Product, Background
from .serializers import ProductSerializer, BackgroundSerializer


class ProductListView(ListAPIView):
    """
    GET /api/products/
    쿼리 파라미터: ?gender=FEMALE&category=백팩&is_new=true
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.all()
        gender = self.request.query_params.get('gender')
        category = self.request.query_params.get('category')
        is_new = self.request.query_params.get('is_new')

        if gender:
            qs = qs.filter(gender=gender)
        if category:
            qs = qs.filter(category=category)
        if is_new:
            qs = qs.filter(is_new=is_new.lower() == 'true')
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        # 인기 TOP3: 선택 횟수 기준
        top3 = Product.objects.order_by('-choose_count')[:3]

        return Response({
            "top3": ProductSerializer(top3, many=True, context={'request': request}).data,
            "products": ProductSerializer(qs, many=True, context={'request': request}).data,
            "filters": {
                "genders": list(Product.objects.values_list('gender', flat=True).distinct()),
                "categories": list(Product.objects.values_list('category', flat=True).distinct()),
            },
        })


class BackgroundListView(ListAPIView):
    """
    GET /api/backgrounds/
    쿼리 파라미터: ?type=나라 별
    """
    serializer_class = BackgroundSerializer

    def get_queryset(self):
        qs = Background.objects.all()
        bg_type = self.request.query_params.get('type')
        if bg_type:
            qs = qs.filter(type=bg_type)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        # 이달의 테마 TOP3: 선택 횟수 기준
        top3 = Background.objects.order_by('-choose_count')[:3]

        return Response({
            "top3": BackgroundSerializer(top3, many=True, context={'request': request}).data,
            "backgrounds": BackgroundSerializer(qs, many=True, context={'request': request}).data,
        })





class ProductLikeView(APIView):
    """POST /api/products/<id>/like/"""

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        today = timezone.localdate()

        # 오늘 처음 좋아요가 들어온 경우
        if product.today_like_date != today:
            product.today_like_count = 0
            product.today_like_date = today

        # 전체 좋아요
        product.like_count += 1

        # 오늘 좋아요
        product.today_like_count += 1

        product.save(update_fields=[
            "like_count",
            "today_like_count",
            "today_like_date",
        ])

        return Response({
            "message": "추천 반영 완료",
            "product_id": product.id,
            "like_count": product.like_count,
            "today_like_count": product.today_like_count,
        }, status=status.HTTP_200_OK)