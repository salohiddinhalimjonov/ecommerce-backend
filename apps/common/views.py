from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from apps.common.serializers import BannerSerializer
from apps.common.permissions import EditedPermissionClass
from apps.common.models import Banner


class BannerViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass,]
    queryset = Banner.objects.all()

    def get_serializer_class(self):
        return BannerSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context