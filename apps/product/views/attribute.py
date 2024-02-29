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
        if isinstance(attr_list, list):
            for attr in attr_list:
                serializer = AttributeSerializer(data=attr)
                serializer.is_valid(raise_exception=True)
                title = serializer.validated_data.get('title')
                category = serializer.validated_data.get('category')
                attr_instance = Attribute.objects.create(title=title)
                attr_instance.category.set(category)
        else:
            serializer = AttributeSerializer(data=attr_list)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({'status':'Successfully Created!'}, status=status.HTTP_201_CREATED)



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




