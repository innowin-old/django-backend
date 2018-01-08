from rest_framework import permissions


class IsIdentityOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif obj.identity_user.user == request.user or request.user.is_superuser:
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