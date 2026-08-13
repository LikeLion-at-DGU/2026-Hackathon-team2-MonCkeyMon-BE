from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExperienceSession
from .serializers import (
    ExperienceSessionSerializer,
    PhotoUploadSerializer,
    VideoGenerateSerializer,
)


class ExperienceCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session = ExperienceSession.objects.create()
        serializer = ExperienceSessionSerializer(session)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ExperienceDetailView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, session_id):
        session = get_object_or_404(ExperienceSession, id=session_id)

        serializer = ExperienceSessionSerializer(
            session,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PhotoUploadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, session_id):
        session = get_object_or_404(ExperienceSession, id=session_id)

        if session.background is None:
            return Response(
                {"detail": "배경을 선택한 뒤 사진을 업로드할 수 있습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PhotoUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session.person_image = serializer.validated_data["person_image"]
        session.save()

        # AI 합성 전 임시 처리:
        # 현재는 원본 사진을 composite_image로 사용합니다.
        # delivery의 실제 합성 로직이 완성되면 이 부분을 교체합니다.
        session.composite_image = session.person_image.name
        session.status = "PHOTO_DONE"
        session.save(update_fields=["composite_image", "status"])

        composite_image_url = request.build_absolute_uri(
            session.composite_image.url
        )

        return Response(
            {
                "message": "사진 업로드 완료",
                "composite_image": composite_image_url,
                "status": session.status,
            },
            status=status.HTTP_200_OK,
        )


class VideoGenerateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, session_id):
        session = get_object_or_404(ExperienceSession, id=session_id)

        if session.background is None or session.product is None:
            return Response(
                {"detail": "배경과 제품을 모두 선택한 뒤 영상을 생성할 수 있습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not session.person_image:
            return Response(
                {"detail": "사진을 업로드한 뒤 영상을 생성할 수 있습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if session.status == "PROCESSING":
            return Response(
                {"detail": "이미 영상 생성이 진행 중입니다."},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = VideoGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session.guide_action = serializer.validated_data.get("guide_action")
        session.status = "PROCESSING"
        session.save(update_fields=["guide_action", "status"])

        # 교현님이 delivery/services.py에 generate_video_task를 만들면
        # 여기에서 실제 AI 영상 생성 작업을 호출합니다.

        return Response(
            {
                "message": "AI 영상 생성이 시작되었습니다.",
                "status": session.status,
            },
            status=status.HTTP_200_OK,
        )


class ExperienceStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, session_id):
        session = get_object_or_404(ExperienceSession, id=session_id)

        response_data = {
            "status": session.status,
        }

        if session.status == "COMPLETED":
            try:
                video = session.video
            except Exception:
                video = None

            if video and video.video_file:
                response_data.update(
                    {
                        "session_id": str(session.id),
                        "video_url": request.build_absolute_uri(
                            video.video_file.url
                        ),
                        "share_url": request.build_absolute_uri(
                            f"/api/share/{session.id}/"
                        ),
                    }
                )

        return Response(response_data, status=status.HTTP_200_OK)