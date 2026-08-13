from django.urls import path
from .views import ProductListView, BackgroundListView, ProductLikeView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('backgrounds/', BackgroundListView.as_view(), name='background-list'),
    path('products/<int:pk>/like/', ProductLikeView.as_view(), name='product-like'),
]