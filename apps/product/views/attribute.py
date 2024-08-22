from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from apps.product.serializers.attribute import AttributeSerializer, AttributeValueSerializer
from apps.product.models import Attribute, AttributeValue
from apps.common.permissions import EditedPermissionClass


class AttributeViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def create(self, request, *args, **kwargs):
        attr_list = request.data.get('attr_list')
        if attr_list is None:
            return Response({'status': 'Attr List is None'}, status=status.HTTP_400_BAD_REQUEST)
        values = None
        for attr in attr_list:
            if attr.get('values'):
                values = attr.pop('values')
            serializer = AttributeSerializer(data=attr)
            serializer.is_valid(raise_exception=True)
            title = serializer.validated_data.get('title')
            category = serializer.validated_data.get('category')
            attr_instance = Attribute.objects.create(title=title)
            attr_instance.category.set(category)
            if values:
                for value in values:
                    AttributeValue.objects.create(attribute=attr_instance, value=value)
        return Response({'status':'Successfully Created!'}, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        values = None
        if request.data.get('values'):
            values = request.data.pop('values')
        instance = self.get_object()
        serializer = AttributeSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        #title = serializer.validated_data.get('title')
        #category = serializer.validated_data.get('category')
        serializer.save()
        #attr_instance.category.set(category)
        if values:
            AttributeValue.objects.filter(attribute=instance).delete()
            for value in values:
                AttributeValue.objects.create(attribute=instance, value=value)
        return Response({'status': 'Successfully Updated!'}, status=status.HTTP_201_CREATED)


class AttributeValueViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        attribute = serializer.validated_data.get('attribute')
        values = serializer.validated_data.get('value')
        for value in values:
            AttributeValue.objects.create(attribute=attribute, value=value)
        return Response({'status': 'Successfully created!'}, status=status.HTTP_201_CREATED)




