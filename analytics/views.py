from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from products.models import Product, Background


class ChooseCountView(APIView):

    def get(self, request):
        products = Product.objects.values(
            'id',
            'name',
            'choose_count'
        )

        backgrounds = Background.objects.values(
            'id',
            'name',
            'choose_count'
        )

        return Response({
            'products': products,
            'backgrounds': backgrounds,
        })

class ChooseCountTop5View(APIView):

    def get(self, request):
        products = Product.objects.order_by(
            '-choose_count'
        ).values(
            'id',
            'name',
            'choose_count'
        )[:5]

        backgrounds = Background.objects.order_by(
            '-choose_count'
        ).values(
            'id',
            'name',
            'choose_count'
        )[:5]

        return Response({
            'products': products,
            'backgrounds': backgrounds,
        })

class ProductLikeCountView(APIView):

    def get(self, request):
        products = Product.objects.values(
            'id',
            'name',
            'like_count'
        )

        return Response({
            'products': products,
        })