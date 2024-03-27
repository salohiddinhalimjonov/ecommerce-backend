from rest_framework import serializers
from django.db.models import Avg
from django.db.models.functions import Coalesce
from apps.product.models import Product, ProductVariant, ProductVariantImage
from apps.product.services.product_variant import get_price_with_discount


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'image',
            'title',
            'price',
            'is_available',
            'category',
            'is_new'
        ]

    def create(self, validated_data):
        price = validated_data.pop('price')
        if isinstance(price, str) and price.isdigit():
            price = int(price)
        product = Product.objects.create(price=price, **validated_data)
        return product

    def update(self, instance: Product, validated_data):
        price = validated_data.pop('price')
        if isinstance(price, str) and price.isdigit():
            price = int(price)
        instance.image = validated_data.get('image')
        instance.price = validated_data.get('price')
        instance.is_available = validated_data.get('is_available')
        instance.category = validated_data.get('category')
        instance.is_new = validated_data.get('is_new')
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            image_url = instance.image.url
            representation['image'] = request.build_absolute_uri(image_url)
        return representation


class ProductVariantSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=serializers.ImageField())
    price_with_discount = serializers.SerializerMethodField()
    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'is_available',
            'title',
            'images',
            'attribute_value',
            'product',
            'other_detail',
            'price',
            'price_with_discount',
            'quantity'
        ]

    def create(self, validated_data):
        images = validated_data.pop('images')
        p_variant = ProductVariant.objects.create(**validated_data)
        order = 1
        for image in images:
            ProductVariantImage.objects.create(product_variant=p_variant, image=image, order=order)
            order += 1
        return p_variant

    def update(self, instance: ProductVariant, validated_data):
        images = validated_data.get('images')
        instance.is_available = validated_data.is_available
        instance.attribute_value.set(validated_data.attribute_value)
        instance.product = validated_data.product
        instance.other_detail = validated_data.other_detail
        instance.price = validated_data.price
        instance.quantity = validated_data.quantity
        instance.save()
        ProductVariantImage.objects.filter(product_variant=instance).delete()
        order = 1
        for image in images:
            ProductVariantImage.objects.create(product_variant=p_variant, image=image, order=order)
            order += 1
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        images = ProductVariantImage.objects.filter(product_variant=instance)
        image_urls = [request.build_absolute_uri(image.url) for image in images]
        representation['images'] = image_urls
        return representation

    def get_price_with_discount(self, obj):
        return get_price_with_discount(obj, user=self.context['request'].user)


# class ProductVariantListSerializer(serializers.ModelSerializer):
#     reviews_count = serializers.SerializerMethodField()
#     reviews_avg = serializers.SerializerMethodField()
#     price_with_discount = serializers.SerializerMethodField()
#     price_in_som = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = ProductVariant
#         exclude = (
#             'created_datetime',
#             'modified_datetime',
#         )
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         request = self.context.get('request')
#         if instance.image:
#             image_url = instance.image.url
#             representation['image'] = request.build_absolute_uri(image_url)
#         return super(ProductVariantListSerializer, self).to_representation(instance)
#
#     def get_reviews_count(self, instance):
#         return instance.reviews.count()
#
#     def get_reviews_avg(self, instance):
#         return instance.reviews.aggregate(avg_rate=Coalesce(Avg('stars'), 0.0))['avg_rate']
#
#     def get_price_with_discount(self, obj):
#         return get_price_with_discount(obj, user=self.context['request'].user)
