from rest_framework import permissions
from .models import Identity

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
        elif request.user:
            return True
        return False