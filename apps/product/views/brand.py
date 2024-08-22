from rest_framework.viewsets import ModelViewSet
from apps.product.models import Brannd
from apps.common.permissions import EditedPermissionClass
from apps.product.serializers.brand import BrandSerializer, BrandGetSerializer


class BrandViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    queryset = Brannd.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BrandGetSerializer
        else:
            return BrandSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

