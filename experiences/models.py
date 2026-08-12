import uuid
from django.db import models
from products.models import Product, Background

class ExperienceSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 선택 정보
    background = models.ForeignKey(Background, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    
    # 이미지 파일
    person_image = models.ImageField(upload_to='persons/', null=True, blank=True)          # 원본 사진
    composite_image = models.ImageField(upload_to='composites/', null=True, blank=True)    # ✨ 추가: 배경 합성 사진
    
    # AI 가이드 및 전화번호
    guide_action = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    # 세션 상태 (START -> PHOTO_DONE -> PROCESSING -> COMPLETED -> FAILED)
    status = models.CharField(max_length=20, default='START')

    def __str__(self):
        return f"Session {self.id} - {self.status}"