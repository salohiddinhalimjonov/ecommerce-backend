from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions, filters
from apps.product.models import Product, ProductVariant
from apps.common.permissions import EditedPermissionClass
from apps.product.serializers.product import ProductSerializer, ProductVariantSerializer
from apps.product.filters import ProductVariantFilter


class ProductViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [SearchFilter,]
    search_fields = ['title',]


class ProductVariantViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUser,]
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product',]
    search_fields = ['title',]
    ordering_fields = ['product__title',]


class ProductVariantListAPIView(ListAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.AllowAny,]
    filterset_class = ProductVariantFilter
    search_fields = ['title',]
    ordering_fields = ['price', 'created_at']

