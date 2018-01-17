from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or request.user.is_superuser:
            return True
        return False


class BlockPostMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner_field_name = view.owner_field
        if getattr(obj, owner_field_name) == request.user or request.user.is_superuser:
            return True
        return False