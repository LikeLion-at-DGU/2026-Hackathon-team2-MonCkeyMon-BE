from django.db.models import Count
from django.db.models.functions import TruncDate

from rest_framework.views import APIView
from rest_framework.response import Response

from experiences.models import ExperienceSession
from products.models import Product, Background


from django.db.models import F, IntegerField, ExpressionWrapper
from django.db.models import Sum

from .serializers import (
    ProductChooseCountSerializer,
    BackgroundChooseCountSerializer,
    ProductLikeCountSerializer,
    TotalVisitorCountSerializer,
    DailyVisitorCountSerializer,
    ProductInterestSerializer,
    CategorySessionTopSerializer,
    ProductSessionSerializer,
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
    

class ProductInterestView(APIView):

    def get(self, request):
        products = (
            Product.objects
            .annotate(
                total_score=ExpressionWrapper(
                    F('choose_count') * 1
                    + F('link_count') * 3
                    + F('like_count') * 5,
                    output_field=IntegerField(),
                )
            )
            .order_by('-total_score')
        )

        data = []

        for rank, product in enumerate(products, start=1):
            data.append({
                'rank': rank,
                'product_id': product.id,
                'product_name': product.name,

                'color': product.color,
                'size': product.size,
                'gender': product.gender,
                'category': product.category,

                'session_count': product.choose_count,
                'link_received_count': product.link_count,
                'link_click_count': product.like_count,
                'total_score': product.total_score,
            })

        serializer = ProductInterestSerializer(
            data,
            many=True
        )

        return Response(serializer.data)

class CategorySessionTop5View(APIView):

    def get(self, request):
        categories = (
            Product.objects
            .values('category')
            .annotate(
                session_count=Sum('choose_count')
            )
            .order_by('-session_count')[:5]
        )

        data = []

        for rank, category in enumerate(categories, start=1):
            data.append({
                'rank': rank,
                'category': category['category'],
                'session_count': category['session_count'],
            })

        serializer = CategorySessionTopSerializer(
            data,
            many=True
        )

        return Response(serializer.data)
    
class ProductSessionView(APIView):

    def get(self, request):
        products = Product.objects.all()

        search = request.query_params.get('search')
        is_new = request.query_params.get('is_new')

        if search:
            products = products.filter(name__icontains=search)
        if is_new:
            products = products.filter(is_new=is_new.lower() == 'true')

        products = products.order_by('-choose_count')

        serializer = ProductSessionSerializer(
            products,
            many=True
        )

        return Response(serializer.data)