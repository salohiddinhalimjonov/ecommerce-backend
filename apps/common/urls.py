from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.common.views import BannerViewSet

router = DefaultRouter()
router.register('banner', BannerViewSet, basename='banner')

urlpatterns = [
    path('', include(router.urls)),
]