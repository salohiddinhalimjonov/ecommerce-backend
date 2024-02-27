from rest_framework import serializers
from apps.product.models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'image',
            'children'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)
        else:
            return None

    def get_children(self, obj):
        if obj.level == 1:
            return obj.children.all().values('id', 'title')
        else:
            return None


class CategoryDetailSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'parent'
        ]
        extra_kwargs = {
            'parent': {
                'required': False
            }
        }
    def get_parent(self, obj):
        if obj.level == 1:
            return None
        else:
            data = {'id': obj.parent.id, 'title': obj.parent.title}
            return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'image',
            'parent'
        ]
        extra_kwargs = {
            'parent': {
                'required': False
            },
            'image': {
                'required': False
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            image_url = instance.image.url
            representation['image'] = request.build_absolute_uri(image_url)
        return representation
