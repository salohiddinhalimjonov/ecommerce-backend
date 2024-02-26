from rest_framework.viewsets import ModelViewSet
from apps.product.models import Brannd
from apps.common.permissions import EditedPermissionClass
from apps.product.serializers.brand import BrandSerializer


class BrandView(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    queryset = Brannd.objects.all()
    serializer_class = BrandSerializer