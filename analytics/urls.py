from django.urls import path
from .views import ChooseCountView, ChooseCountTop5View, ProductLikeCountView, TotalVisitorCountView, DailyVisitorCountView

urlpatterns = [
    path(
        'choose-count/',
        ChooseCountView.as_view(),
        name='choose-count'
    ),
    path(
        'choose-count/top5/',
        ChooseCountTop5View.as_view(),
        name='choose-count-top5'
    ),
    path(
        'like-count/',
        ProductLikeCountView.as_view(),
        name='product-like-count'
    ),
    path(
    'visitor-count/',
    TotalVisitorCountView.as_view(),
    name='visitor-count'
    ),

    path(
        'visitor-count/daily/',
        DailyVisitorCountView.as_view(),
        name='visitor-count-daily'
    ),
    
]