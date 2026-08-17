from django.db.models import Count
from django.db.models.functions import TruncDate

from rest_framework.views import APIView
from rest_framework.response import Response

from experiences.models import ExperienceSession
from products.models import Product, Background

from .serializers import (
    ProductChooseCountSerializer,
    BackgroundChooseCountSerializer,
    ProductLikeCountSerializer,
    TotalVisitorCountSerializer,
    DailyVisitorCountSerializer,
)

class ChooseCountView(APIView):

    def get(self, request):
        products = ProductChooseCountSerializer(
            Product.objects.all(),
            many=True
        ).data

        backgrounds = BackgroundChooseCountSerializer(
            Background.objects.all(),
            many=True
        ).data

        return Response({
            'products': products,
            'backgrounds': backgrounds,
        })


class ChooseCountTop5View(APIView):

    def get(self, request):
        products = ProductChooseCountSerializer(
            Product.objects.order_by('-choose_count')[:5],
            many=True
        ).data

        backgrounds = BackgroundChooseCountSerializer(
            Background.objects.order_by('-choose_count')[:5],
            many=True
        ).data

        return Response({
            'products': products,
            'backgrounds': backgrounds,
        })


class ProductLikeCountView(APIView):

    def get(self, request):
        products = ProductLikeCountSerializer(
            Product.objects.all(),
            many=True
        ).data

        return Response({
            'products': products,
        })


class TotalVisitorCountView(APIView):

    def get(self, request):
        count = ExperienceSession.objects.count()

        serializer = TotalVisitorCountSerializer({
            'total_visitor_count': count
        })

        return Response(serializer.data)


class DailyVisitorCountView(APIView):

    def get(self, request):
        data = (
            ExperienceSession.objects
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        serializer = DailyVisitorCountSerializer(
            data,
            many=True
        )

        return Response(serializer.data)