from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from apps.product.serializers.attribute import AttributeSerializer
from apps.product.models import Attribute


class AttributeViewSet(ModelViewSet):
    permission_classes = [IsAdminUser,]
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


