from rest_framework import permissions
from django.contrib.auth.models import User


class IsIdentityOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif obj.identity_user == request.user or request.user.is_superuser:
            return True
        return False


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif not obj.is_superuser:
            return True
        elif request.user.is_superuser:
            return True
        return False


class IsUrlOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif obj.identity_url_related_identity.identity_user == request.user or request.user.is_superuser:
            return True
        return False


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        elif request.user.is_authenticated:
            return True
        return False


class IsDeviceOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            device_user_id = request.POST.get('device_user', None)
            if device_user_id is not None:
                if device_user_id.isdigit():
                    try:
                        user = User.objects.get(pk=device_user_id)
                    except User.DoesNotExist:
                        return False
                    if user == request.user:
                        return True
            return False
        return True