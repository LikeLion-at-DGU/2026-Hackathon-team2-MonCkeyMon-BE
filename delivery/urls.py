from django.urls import path
from .views import ShareDetailView, CompositeImageView

urlpatterns = [
    path('share/<uuid:session_id>/', ShareDetailView.as_view(), name='share-detail'),
    path('composite/<uuid:session_id>/', CompositeImageView.as_view(), name='composite-image'),
]