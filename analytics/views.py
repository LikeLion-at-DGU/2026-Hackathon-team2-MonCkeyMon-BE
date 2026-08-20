from django.db.models import Count
from django.db.models.functions import TruncDate

from rest_framework.views import APIView
from rest_framework.response import Response

from experiences.models import ExperienceSession
from products.models import Product, Background

from datetime import date
from django.db.models import F, IntegerField, ExpressionWrapper
from django.db.models import Sum
from django.db.models import Case, When, Value

from .serializers import *

def _with_effective_choose_count(queryset, period):
    if period != 'today':
        return queryset.order_by('-choose_count')

    today = date.today()
    return queryset.annotate(
        effective_choose_count=Case(
            When(today_choose_date=today, then='today_choose_count'),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('-effective_choose_count')


class ChooseCountView(APIView):

    def get(self, request):
        period = request.query_params.get('period')

        products = ProductChooseCountSerializer(
            _with_effective_choose_count(Product.objects.all(), period),
            many=True,
            context={'period': period},
        ).data

        backgrounds = BackgroundChooseCountSerializer(
            _with_effective_choose_count(Background.objects.all(), period),
            many=True,
            context={'period': period},
        ).data

        return Response({
            'products': products,
            'backgrounds': backgrounds,
        })


class ChooseCountTop5View(APIView):

    def get(self, request):
        period = request.query_params.get('period')

        products = ProductChooseCountSerializer(
            _with_effective_choose_count(Product.objects.all(), period)[:5],
            many=True,
            context={'period': period},
        ).data

        backgrounds = BackgroundChooseCountSerializer(
            _with_effective_choose_count(Background.objects.all(), period)[:5],
            many=True,
            context={'period': period},
        ).data

        return Response({
            'products': products,
            'backgrounds': backgrounds,
        })


class ProductLikeCountView(APIView): # 상품 별 구매 링크 클릭 횟수

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
        count = Product.objects.aggregate(
            total=Sum('choose_count')
        )['total'] or 0

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

        serializer = DailyVisitorCountSerializer(data, many=True)
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
        period = request.query_params.get('period')

        if period == 'today':
            today = date.today()
            products = Product.objects.annotate(
                effective_choose_count=Case(
                    When(today_choose_date=today, then='today_choose_count'),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            categories = (
                products
                .values('category')
                .annotate(session_count=Sum('effective_choose_count'))
                .order_by('-session_count')[:5]
            )
        else:
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
        period = request.query_params.get('period')  # 'today' 또는 미지정(누적)

        if search:
            products = products.filter(name__icontains=search)
        if is_new:
            products = products.filter(is_new=is_new.lower() == 'true')

        if period == 'today':
            today = date.today()
            products = products.annotate(
                effective_session_count=Case(
                    When(today_choose_date=today, then='today_choose_count'),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).order_by('-effective_session_count')
        else:
            products = products.order_by('-choose_count')

        serializer = ProductSessionSerializer(
            products,
            many=True,
            context={'period': period},
        )

        return Response(serializer.data)


class TotalLinkAnalyticsView(APIView): # 전체 구매 링크 클릭 횟수, 전체 링크 받기 한 수

    def get(self, request):
        total_link_received = (
            Product.objects.aggregate(
                total=Sum("link_count")
            )["total"] or 0
        )

        total_link_click = (
        Product.objects.aggregate(
            total=Sum("like_count")
            )["total"] or 0
        )

        serializer = TotalLinkAnalyticsSerializer({
            "total_link_received": total_link_received,
            "total_link_click": total_link_click,
        })

        return Response(serializer.data)

class TodayLikeCountView(APIView): # 구매 링크 클릭 횟수(하루)

    def get(self, request):
        today = date.today()

        today_like_count = (
            Product.objects.filter(today_like_date=today).aggregate(
                total=Sum("today_like_count")
            )["total"] or 0
        )

        serializer = TodayLikeCountSerializer({
            "today_click_count": today_like_count,
        })

        return Response(serializer.data)


class TodayLinkCountView(APIView): # 링크 받기 한 수(하루)

    def get(self, request):
        today = date.today()

        today_link_count = (
            Product.objects.filter(today_link_date=today).aggregate(
                total=Sum("today_link_count")
            )["total"] or 0
        )

        serializer = TodayLinkCountSerializer({
            "today_link_count": today_link_count,
        })

        return Response(serializer.data)

class TodayVisitorCountView(APIView):

    def get(self, request):
        today = date.today()

        today_visitor_count = (
            Product.objects.filter(today_choose_date=today).aggregate(
                total=Sum('today_choose_count')
            )['total'] or 0
        )

        serializer = TodayVisitorCountSerializer({
            "today_visitor_count": today_visitor_count,
        })

        return Response(serializer.data)