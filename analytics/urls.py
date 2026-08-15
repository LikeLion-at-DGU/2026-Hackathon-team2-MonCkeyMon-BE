from django.urls import path
from .views import ChooseCountView, ChooseCountTop5View, ProductLikeCountView

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
]