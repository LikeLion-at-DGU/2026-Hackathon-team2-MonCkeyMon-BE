import logging

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile

from experiences.models import ExperienceSession
from .serializers import ShareDetailSerializer
from .imageservice import generate_composite_image

logger = logging.getLogger(__name__)


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

        if session.product is None or session.background is None:
            return Response(
                {"detail": "배경과 상품을 모두 선택한 뒤 합성할 수 있습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not session.person_image:
            return Response(
                {"detail": "사진을 업로드한 뒤 합성할 수 있습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            image_bytes = generate_composite_image(session)
        except Exception:
            logger.exception(
                "합성 이미지 생성 실패: session_id=%s", session_id
            )
            return Response(
                {"detail": "이미지 합성에 실패했습니다. 잠시 후 다시 시도해주세요."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

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