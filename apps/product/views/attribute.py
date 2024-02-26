from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from apps.product.serializers.attribute import AttributeSerializer
from apps.product.models import Attribute
from apps.common.permissions import EditedPermissionClass


class AttributeViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


