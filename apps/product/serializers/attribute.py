from rest_framework import serializers
from apps.product.models import Attribute, AttributeValue


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = [
            'id',
            'title',
            'category'
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.category:
            representation['category_title'] = instance.category.all().values('title')
        return representation


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = [
            'id',
            'attribute',
            'value'
        ]
        extra_kwargs = {
            'attribute': {'required': True},
            'value': {'required': False}
        }
