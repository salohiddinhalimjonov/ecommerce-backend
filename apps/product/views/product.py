from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions, filters
from apps.product.models import Product, ProductVariant, ProductVariantImage
from apps.common.permissions import EditedPermissionClass
from apps.product.serializers.product import ProductSerializer, ProductVariantSerializer, ProductVariantImageSerializer, ProductCustomListSerializer
from apps.product.filters import ProductVariantFilter


class ProductViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [SearchFilter,]
    search_fields = ['title',]


class ProductCustomListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCustomListSerializer
    permission_classes = [permissions.AllowAny,]


class ProductVariantViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductVariantFilter
    filterset_fields = ['product',]
    search_fields = ['title',]
    ordering_fields = ['product__title',]

    def get_serializer_class(self):
        return ProductVariantSerializer

    # def perform_create(self, serializer):
    #     data = ProductVariant(self.request.data)
    #     data.is_valid(raise_exception=True)
    #     serializer.create(data.validated_data)
    #
    # def perform_update(self, serializer):
    #     serializer.update()


class ProductVariantListAPIView(ListAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.AllowAny,]
    filterset_class = ProductVariantFilter
    search_fields = ['title',]
    ordering_fields = ['price', 'created_at']


class ProductVariantImageViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass, ]
    serializer_class = ProductVariantImageSerializer
    queryset = ProductVariantImage.objects.all()