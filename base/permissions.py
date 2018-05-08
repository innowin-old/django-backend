from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from exchanges.models import Exchange
from users.models import Identity


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
        if request.method == 'GET':
            return True
        owner_field_name = view.owner_field
        if getattr(obj, owner_field_name) == request.user or request.user.is_superuser:
            return True
        return False


class IsRollOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner_object = ContentType.objects.get(model=obj.roll_owner.child_name).__str__()
        child_obj = getattr(obj.roll_owner, owner_object)
        if child_obj.owner == request.user or request.user.is_superuser:
            return True
        return False


class IsRollPermissionOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner_object = ContentType.objects.get(model=obj.roll_permission_related_roll.roll_owner.child_name).__str__()
        child_obj = getattr(obj.roll_permission_related_roll.roll_owner, owner_object)
        print(child_obj.owner)
        if child_obj.owner == request.user or request.user.is_superuser:
            return True
        return False


class IfExchangeIsAcceptedOrNotAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            post_parent_id = request.POST['comment_parent']
            try:
                exchange = Exchange.objects.get(pk=post_parent_id)
            except Exchange.DoesNotExist:
                return True
            permission = IsAcceptedOrNotAccess()
            return permission.has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        parent_field = view.parent_field
        if request.method == 'GET':
            return True
        post_parent_id = request.POST[parent_field]
        try:
            exchange = Exchange.objects.get(pk=post_parent_id)
        except Exchange.DoesNotExist:
            return True
        permission = IsAcceptedOrNotAccess()
        return permission.has_permission(request, view)


class IsAcceptedOrNotAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            identity = Identity.objects.get(identity_user=request.user)
        except Identity.DoesNotExist:
            return False
        if not identity.accepted:
            return False
        return True


class SafeMethodsOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False