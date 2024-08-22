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


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            image_url = instance.image.url
            representation['image'] = request.build_absolute_uri(image_url)
        return representation

class ProductCustomListSerializer(serializers.ModelSerializer):
    product_variant = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'image',
            'title',
            'price',
            'is_available',
            'category',
            'is_new',
            'product_variant'
        ]

    def get_product_variant(self, obj):
        product_variants = obj.product_variant.all()
        serializer = ProductVariantSerializer(product_variants, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            image_url = instance.image.url
            representation['image'] = request.build_absolute_uri(image_url)
        return representation



class ProductImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    order = serializers.IntegerField()


class ProductVariantSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=ProductImageSerializer(), required=False, allow_null=True)
    price_with_discount = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'is_available',
            'title',
            'images',
            'product',
            'attribute_value',
            'other_detail',
            'price',
            'price_with_discount',
            'quantity'
        ]


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        images = ProductVariantImage.objects.filter(product_variant=instance)
        image_urls = [{'image':request.build_absolute_uri(image.image.url), 'image_id': image.id} for image in images if image.image]
        representation['images'] = image_urls
        return representation

    def get_price_with_discount(self, obj):
        return get_price_with_discount(obj, user=self.context['request'].user)

    def create(self, validated_data):
        images = validated_data.pop('images')
        #product = Product.objects.get(id=validated_data.pop('product'))
        attribute_value = validated_data.pop('attribute_value')
        p_variant = ProductVariant.objects.create(**validated_data)
        p_variant.attribute_value.set(attribute_value)

        if images:
            for image in images:
                a = ProductVariantImage.objects.create(product_variant=p_variant, image=image['image'], order=image['order'])
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
        for image in images:
            ProductVariantImage.objects.create(product_variant=p_variant, image=image['image'], order=image['order'])
        return instance



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

class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            image_url = instance.image.url
            representation['image'] = request.build_absolute_uri(image_url)
        return representation