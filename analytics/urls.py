from django.urls import path
from .views import *
urlpatterns = [
    path('choose-count/', ChooseCountView.as_view(), name='choose-count'),
    path('choose-count/top5/', ChooseCountTop5View.as_view(), name='choose-count-top5'),
    path('like-count/', ProductLikeCountView.as_view(), name='product-like-count'),
    path('visitor-count/', TotalVisitorCountView.as_view(), name='visitor-count'),
    path('visitor-count/daily/', DailyVisitorCountView.as_view(), name='visitor-count-daily'),
    path('product-interest/', ProductInterestView.as_view(), name='product-interest'),
    path('category-session/top5/', CategorySessionTop5View.as_view(), name='category-session-top5'),
    path('product-session/', ProductSessionView.as_view(), name='product-session'),
    path('total-link/', TotalLinkAnalyticsView.as_view(), name='total-link-analytics'),
    path('today-click-count/', TodayLikeCountView.as_view(), name='today-click-count'),
    path('today-link-count/', TodayLinkCountView.as_view(), name='today-link-count'),
]