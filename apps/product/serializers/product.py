from rest_framework import serializers
from apps.product.models import Product, ProductVariant


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'image',
            'price',
            'is_available',
            'category',
            'is_new'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            image_url = instance.image.url
            representation['image'] = request.build_absolute_uri(image_url)
        return representation


class ProductVariantSerializer(serializers.ModelsSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'is_available',
            'attribute_value',
            'product',
            'other_detail',
            'price',
            'quantity'
        ]
