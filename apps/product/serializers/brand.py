from rest_framework import serializers
from apps.product.models import Brannd


class BrandGetSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Brannd
        fields = [
            'id',
            'title',
            'image'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)
        else:
            return None


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brannd
        fields = [
            'id',
            'title',
            'image'
        ]
        extra_kwargs = {
            'title': {
                'required': True
            },
            'image': {
                'required': True
            }
        }