from rest_framework import serializers
from experiences.models import ExperienceSession


class ShareDetailSerializer(serializers.ModelSerializer):
    session_id = serializers.UUIDField(source='id', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    background_id = serializers.IntegerField(source='background.id', read_only=True)

    product_name = serializers.CharField(source='product.name', read_only=True)

    person_image_url = serializers.SerializerMethodField()
    background_image_url = serializers.SerializerMethodField()
    product_image_url = serializers.SerializerMethodField()
    product_purchase_url = serializers.SerializerMethodField()
    composite_image_url = serializers.SerializerMethodField()

    link_received = serializers.BooleanField(read_only=True)

    class Meta:
        model = ExperienceSession
        fields = [
            'session_id',
            'product_id',
            'background_id',
            'composite_image_url',
            'person_image_url',
            'background_image_url',
            'product_name',
            'product_image_url',
            'product_purchase_url',
            'link_received',
        ]

    def get_composite_image_url(self, obj):
        request = self.context.get('request')

        if obj.composite_image:
            return (
                request.build_absolute_uri(obj.composite_image.url)
                if request
                else obj.composite_image.url
            )

        return None

    def get_person_image_url(self, obj):
        request = self.context.get('request')

        if obj.person_image:
            return (
                request.build_absolute_uri(obj.person_image.url)
                if request
                else obj.person_image.url
            )

        return None

    def get_background_image_url(self, obj):
        request = self.context.get('request')

        if obj.background and obj.background.image:
            return (
                request.build_absolute_uri(obj.background.image.url)
                if request
                else obj.background.image.url
            )

        return None

    def get_product_image_url(self, obj):
        request = self.context.get('request')

        if obj.product and obj.product.overlay_image:
            return (
                request.build_absolute_uri(obj.product.overlay_image.url)
                if request
                else obj.product.overlay_image.url
            )

        return None

    def get_product_purchase_url(self, obj):
        if obj.product and obj.product.purchase_url:
            return obj.product.purchase_url

        return None