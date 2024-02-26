
from rest_framework import permissions


class EditedPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False