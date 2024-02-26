from rest_framework import serializers
from apps.product.models import Brannd


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


