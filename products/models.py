from django.db import models

class Product(models.Model):
    # 성별 선택지
    GENDER_CHOICES = [
        ('FEMALE', '여성'),
        ('MALE', '남성'),
        ('UNISEX', '공용'),
    ]

    name = models.CharField(max_length=100)
    overlay_image = models.ImageField(upload_to='products/overlays/')  # 누끼 딴 PNG
    
    #  필터링용 필드 추가
    season = models.CharField(max_length=20, default='26 SS')   # 예: '26 SS', '25 FW', '25 SS' 등
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='FEMALE') # 여성 / 남성 / 공용
    category = models.CharField(max_length=50, default='숄더백') # 숄더백, 호보백, 미니백, 백팩 등
    purchase_url = models.CharField(max_length=500, blank=True, null=True) # 구매링크
    is_new = models.BooleanField(default=False)   # 신상 여부
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"[{self.season}] {self.name} ({self.category})"
     
class Background(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='backgrounds/')
    type = models.CharField(max_length=50)  # 예: CURATION, KEYWORD 등

    def __str__(self):
        return self.name