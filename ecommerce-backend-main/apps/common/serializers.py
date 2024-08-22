from rest_framework import serializers
from apps.common.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            image_url = instance.image.url
            representation['image'] = request.build_absolute_uri(image_url)
        return representation