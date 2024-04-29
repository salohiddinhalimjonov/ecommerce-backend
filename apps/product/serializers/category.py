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
        request = self.context.get('request')
        if obj.level == 1:
            child_list = []
            for child in obj.children.all():
                if child.image:
                    child_list.append({'id': child.id, 'title': child.title, 'image': request.build_absolute_uri(child.image.url)})
                else:
                    child_list.append({'id': child.id, 'title': child.title, 'image':None})
            return child_list

        else:
            return None


class CategoryDetailSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'image',
            'parent',
            'children'
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            image_url = instance.image.url
            representation['image'] = request.build_absolute_uri(image_url)
            attributes = [{'id': attribute.id,
                           'title': attribute.title,
                           'values': attribute.values_hi.values('id', 'value')}
                          for attribute in instance.attributes.all()]
            representation['attributes'] = attributes
        return representation

    def get_children(self, obj):
        request = self.context.get('request')
        if obj.level == 1:
            child_list = []
            for child in obj.children.all():
                if child.image:
                    child_list.append({'id': child.id, 'title': child.title, 'image': request.build_absolute_uri(child.image.url)})
                else:
                    child_list.append({'id': child.id, 'title': child.title, 'image':None})
            return child_list

        else:
            return None


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


class SubCategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'image'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        parent = {'id': instance.parent.id, 'title': instance.parent.title}
        if instance.image:
            image_url = instance.image.url
            representation['id'] = instance.id
            representation['title'] = instance.title
            representation['image'] = request.build_absolute_uri(image_url)
            representation['parent'] = parent
        return representation

class CategoryAttributeValueSerializer(serializers.Serializer):
    value_id = serializers.IntegerField(allow_null=True)
    value = serializers.CharField()


class CategoryAttributeSerializer(serializers.Serializer):
    attribute_id = serializers.IntegerField(allow_null=True)
    title = serializers.CharField()
    values = serializers.ListSerializer(child=CategoryAttributeValueSerializer())


class CategoryAttributeListUpdateSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    attributes = serializers.ListSerializer(child=CategoryAttributeSerializer())