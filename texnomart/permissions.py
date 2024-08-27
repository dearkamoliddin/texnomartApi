
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class CustomPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            if request.method == 'DELETE' and request.user.is_superuser:
                return True

            if request.method in ['PATCH', 'PUT'] and request.user.is_staff:
                return True
