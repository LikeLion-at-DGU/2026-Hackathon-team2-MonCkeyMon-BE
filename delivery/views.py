from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile

from experiences.models import ExperienceSession
from .serializers import ShareDetailSerializer
from .imageservice import generate_composite_image


class ShareDetailView(RetrieveAPIView):
    queryset = ExperienceSession.objects.all()
    serializer_class = ShareDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'session_id'


class CompositeImageView(APIView):

    def post(self, request, session_id):
        session = get_object_or_404(
            ExperienceSession,
            id=session_id
        )

        image_bytes = generate_composite_image(session)

        session.composite_image.save(
            f"composite_{session.id}.png",
            ContentFile(image_bytes),
            save=True
        )

        return Response({
            "message": "합성 이미지 생성 완료",
            "image_url": request.build_absolute_uri(
                session.composite_image.url
            )
        })