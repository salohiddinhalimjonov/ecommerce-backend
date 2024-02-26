from rest_framework.viewsets import ModelViewSet
from apps.product.models import Category
from apps.common.permissions import EditedPermissionClass
from apps.product.serializers.category import CategorySerializer


class CategoryView(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer