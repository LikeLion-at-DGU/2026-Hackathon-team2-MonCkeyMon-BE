from rest_framework.generics import RetrieveAPIView
from .models import Video
from .serializers import ShareDetailSerializer

class ShareDetailView(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = ShareDetailSerializer
    lookup_field = 'session_id'  # URL 패턴에서 넘어온 session_id(UUID)로 객체 조회