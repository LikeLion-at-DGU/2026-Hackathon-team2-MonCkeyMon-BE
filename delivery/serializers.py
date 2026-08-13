from rest_framework import serializers
from .models import Video

class ShareDetailSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(source='session.id', read_only=True)
    product_name = serializers.CharField(source='session.product.name', read_only=True)
    video_url = serializers.SerializerMethodField()
    composite_image_url = serializers.SerializerMethodField()
    product_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'session_id',
            'video_url',
            'composite_image_url',
            'product_name',
            'product_image_url',
        ]

    def get_video_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.video_file.url) if request and obj.video_file else None

    def get_composite_image_url(self, obj):
        request = self.context.get('request')
        session = obj.session
        return request.build_absolute_uri(session.composite_image.url) if request and session.composite_image else None

    def get_product_image_url(self, obj):
        request = self.context.get('request')
        product = obj.session.product
        return request.build_absolute_uri(product.overlay_image.url) if request and product and product.overlay_image else None