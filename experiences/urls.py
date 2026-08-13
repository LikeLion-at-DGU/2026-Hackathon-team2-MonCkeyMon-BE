from django.urls import path

from . import views


app_name = "experiences"

urlpatterns = [
    path("", views.ExperienceCreateView.as_view(), name="create"),
    path("<uuid:session_id>/", views.ExperienceDetailView.as_view(), name="detail"),
    path(
        "<uuid:session_id>/upload-photo/",
        views.PhotoUploadView.as_view(),
        name="upload-photo",
    ),
    path(
        "<uuid:session_id>/generate/",
        views.VideoGenerateView.as_view(),
        name="generate",
    ),
    path(
        "<uuid:session_id>/status/",
        views.ExperienceStatusView.as_view(),
        name="status",
    ),
]