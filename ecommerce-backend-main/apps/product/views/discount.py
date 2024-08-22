from rest_framework.viewsets import ModelViewSet
from apps.product.serializers.discount import DiscountSerializer
from apps.product.models import Discount


class DiscountViewSet(ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
