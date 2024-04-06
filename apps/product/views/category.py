from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from apps.product.models import Category, Attribute, AttributeValue
from apps.common.permissions import EditedPermissionClass
from apps.product.serializers.category import (CategorySerializer, CategoryListSerializer, CategoryDetailSerializer, SubCategorySerializer,
                                               CategoryAttributeListUpdateSerializer)


class CategoryViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    filter_backends = [SearchFilter, ]
    search_fields = ['title', ]

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(level=1)
        return Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action == 'retrieve':
            return CategoryDetailSerializer
        else:
            return CategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent = serializer.validated_data.get('parent')
        if isinstance(parent, Category):
            if parent.level != 1:
                return Response({'status':'Parent can not be sub category!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                obj = Category(level=2, **serializer.validated_data)
                obj.save()
        else:
            image = serializer.validated_data.get('image')
            if not image:
                return Response({'status': 'Parent Categories must have an image!'}, status=status.HTTP_400_BAD_REQUEST)
            obj = Category(**serializer.validated_data)
            obj.save()
        serializer = CategorySerializer(obj, context={"request": self.request})

        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer_class()(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        parent = serializer.validated_data.get('parent')
        if isinstance(parent, Category):
            if parent != 1:
                return Response({'status': 'Parent can not be sub category!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                instance.level = 2
                instance.save()
        else:
            image = serializer.validated_data.get('image')
            if not image and not instance.image:
                return Response({'status': 'Parent Categories must have an image!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        serializer = CategorySerializer(instance, context={"request": self.request})
        return Response({'updated_data': serializer.data}, status=status.HTTP_201_CREATED)



class SubCategoryView(ListAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return Category.objects.filter(level=2, parent__isnull=False)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context



class CategoryAttributeEditView(APIView):
    serializer_class = CategoryAttributeListUpdateSerializer

    @swagger_auto_schema(response_body=CategoryAttributeListUpdateSerializer)
    def patch(self, request):
        serializer = CategoryAttributeListUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pk = serializer.validated_data.get('category_id')
        attributes = serializer.validated_data.get('attributes')
        category = get_object_or_404(Category, pk=pk)
        category.attributes.clear()
        for attribute in attributes:
            if attribute['attribute_id']:
                instance = get_object_or_404(Attribute, pk=attribute['attribute_id'])
                instance.title = attribute['title']
                instance.save()
                category.attributes.add(instance)
            else:
                instance = Attribute.objects.create(title=attribute['title'])
                category.attributes.add(instance)

            for value in attribute['values']:
                if value['value_id']:
                    instance_value = get_object_or_404(AttributeValue, pk=value['value_id'])
                    instance_value.value = value['value']
                    instance_value.attribute = instance
                    instance_value.save()
                else:
                    instance_value = AttributeValue.objects.create(attribute=instance, value=value['value'])

        return Response({'status': 'Success'}, status=status.HTTP_201_CREATED)



