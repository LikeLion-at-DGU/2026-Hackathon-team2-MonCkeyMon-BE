from rest_framework.views import APIView
from rest_framework.response import Response
from experiences.models import ExperienceSession
from products.models import Product, Background

from .serializers import (
    ProductChooseCountSerializer,
    BackgroundChooseCountSerializer,
    ProductLikeCountSerializer,
    CompletedExperienceCountSerializer
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


class CompletedExperienceCountView(APIView):

    def get(self, request):
        count = ExperienceSession.objects.exclude(
            composite_image=''
        ).filter(
            composite_image__isnull=False
        ).count()

        serializer = CompletedExperienceCountSerializer({
            'completed_experience_count': count
        })

        return Response(serializer.data)