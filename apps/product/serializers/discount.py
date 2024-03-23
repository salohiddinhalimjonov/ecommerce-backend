from rest_framework import serializers
from apps.product.models import *
from apps.product.serializers.product import ProductSerializer
from apps.product.utils import discount_validators


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

    def validate(self, attrs):
        discount_validators(self.context['request'], attrs)
        return super().validate(attrs)

    def to_representation(self, instance):
        self.fields['products'] = ProductSerializer(many=True, context=self.context)
        self.fields['product_variants'] = ProductVariantListSerializer(many=True, context=self.context)
        return super(DiscountSerializer, self).to_representation(instance)
