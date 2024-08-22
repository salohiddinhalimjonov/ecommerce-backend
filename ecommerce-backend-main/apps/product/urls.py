from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.product.views.attribute import AttributeViewSet, AttributeValueViewSet
from apps.product.views.brand import BrandViewSet
from apps.product.views.discount import DiscountViewSet
from apps.product.views.category import CategoryViewSet, SubCategoryView, CategoryAttributeEditView
from apps.product.views.product import ProductViewSet, ProductVariantViewSet, ProductVariantListAPIView, ProductVariantImageViewSet, ProductCustomListAPIView


router = DefaultRouter()
router.register('attribute', AttributeViewSet, basename='attribute')
router.register('attribute-value', AttributeValueViewSet, basename='attribute_value')
router.register('brand', BrandViewSet, basename='brand')
router.register('discount', DiscountViewSet, basename='discount')
router.register('category', CategoryViewSet, basename='category')
router.register('product', ProductViewSet, basename='product')
router.register('product_variant', ProductVariantViewSet, basename='product_variant')
router.register('product_variant_image', ProductVariantImageViewSet, basename='product_variant_image')


urlpatterns = [
    path('', include(router.urls)),
    path('api/subcategory/', SubCategoryView.as_view(), name='subcategory'),
    path('api/product-variant-list/', ProductVariantListAPIView.as_view(), name='product_variant_list'),
    path('api/category_edit/', CategoryAttributeEditView.as_view(), name='category_edit'),
    path('api/product-custom-list/', ProductCustomListAPIView.as_view(), name='product_custom_list')
]
