from django.db import models

class Product(models.Model):
    GENDER_CHOICES = [
        ('FEMALE', '여성'),
        ('MALE', '남성'),
        ('UNISEX', '공용'),
    ]

    name = models.CharField(max_length=100)
    overlay_image = models.ImageField(upload_to='products/overlays/')

    color = models.CharField(max_length=50, blank=True)      # 예: Soft Pink
    size = models.CharField(max_length=20, blank=True)       # 예: S

    season = models.CharField(max_length=20, default='26 SS')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='FEMALE')
    category = models.CharField(max_length=50, default='숄더백')
    purchase_url = models.CharField(max_length=500, blank=True, null=True)
    is_new = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.color}/{self.size})"


class Background(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='backgrounds/')
    type = models.CharField(max_length=50)
    tags = models.CharField(max_length=200, blank=True)      # 쉼표 구분: "후지산,신사"

    def __str__(self):
        return self.name