from django.db import models


class Product(models.Model):
    GENDER_CHOICES = [
        ('FEMALE', '여성'),
        ('MALE', '남성'),
        ('UNISEX', '공용'),
    ]

    CATEGORY_CHOICES = [
        ('토트백&쇼퍼백', '토트백&쇼퍼백'),
        ('숄더백&크로스백', '숄더백&크로스백'),
        ('백팩', '백팩'),
        ('탑 핸들백', '탑 핸들백'),
        ('트래블', '트래블'),
        ('벨트백', '벨트백'),
        ('미니백', '미니백'),
        ('클러치&파우치', '클러치&파우치'),
    ]

    name = models.CharField(max_length=100)
    overlay_image = models.ImageField(upload_to='products/overlays/')

    color = models.CharField(max_length=50, blank=True)      # 예: Soft Pink
    size = models.CharField(max_length=20, blank=True)       # 예: S

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='FEMALE')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='숄더백&크로스백')
    purchase_url = models.CharField(max_length=500, blank=True, null=True)
    is_new = models.BooleanField(default=False)              # 신상 여부
    like_count = models.PositiveIntegerField(default=0)
    today_like_count = models.PositiveIntegerField(default=0)
    today_like_date = models.DateField(null=True, blank=True)

    choose_count = models.PositiveIntegerField(default=0)
    today_choose_count = models.PositiveIntegerField(default=0)
    today_choose_date = models.DateField(null=True, blank=True)

    link_count = models.PositiveIntegerField(default=0)
    today_link_count = models.PositiveIntegerField(default=0)
    today_link_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} ({self.color}/{self.size})"


class Background(models.Model):
    TYPE_CHOICES = [
        ('나라 별', '나라 별'),
        ('큐레이션룸', '큐레이션룸'),
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='backgrounds/')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='나라 별')
    tags = models.CharField(max_length=200, blank=True)      # 쉼표 구분: "후지산,신사"
    choose_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name