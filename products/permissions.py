from rest_framework import permissions

from users.models import Identity


class IsProductOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if obj.product_owner.identity_user == request.user or request.user.is_superuser:
            return True
        return False