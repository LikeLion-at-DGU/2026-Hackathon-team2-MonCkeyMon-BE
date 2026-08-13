from django.urls import path
from .views import ShareDetailView

urlpatterns = [
    path('share/<uuid:session_id>/', ShareDetailView.as_view(), name='share-detail'),
]