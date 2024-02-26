from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.product.views.attribute import AttributeViewSet


router = DefaultRouter()
router.register('attribute', AttributeViewSet, basename='attribute')

urlpatterns = [
    path('', include(router.urls)),
]
