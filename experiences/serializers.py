from rest_framework import serializers

from products.models import Background, Product
from .models import ExperienceSession


class ExperienceSessionSerializer(serializers.ModelSerializer):
    background_id = serializers.PrimaryKeyRelatedField(
        source="background",
        queryset=Background.objects.all(),
        required=False,
        allow_null=True,
    )
    product_id = serializers.PrimaryKeyRelatedField(
        source="product",
        queryset=Product.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = ExperienceSession
        fields = [
            "id",
            "created_at",
            "background_id",
            "product_id",
            "person_image",
            "composite_image",
            "guide_action",
            "phone_number",
            "status",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "person_image",
            "composite_image",
            "status",
        ]


class PhotoUploadSerializer(serializers.Serializer):
    person_image = serializers.ImageField()


class VideoGenerateSerializer(serializers.Serializer):
    guide_action = serializers.CharField(
        max_length=50,
        required=False,
        allow_null=True,
        allow_blank=True,
    )