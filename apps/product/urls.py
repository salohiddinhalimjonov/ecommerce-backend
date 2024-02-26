from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.product.views.attribute import AttributeViewSet
from apps.product.views.brand import BrandViewSet
from apps.product.views.category import CategoryViewSet


router = DefaultRouter()
router.register('attribute', AttributeViewSet, basename='attribute')
router.register('brand', BrandViewSet, basename='brand')
router.register('category', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
