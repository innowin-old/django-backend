from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from exchanges.models import Exchange
from organizations.models import Organization
from products.models import Product
from users.models import Identity
from .models import Base, BaseRoll


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


class OnlyPostMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        owner_field_name = view.owner_field
        if getattr(obj, owner_field_name) == request.user or request.user.is_superuser:
            return True
        return False


class IsRollOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            base_id = request.POST.get('roll_owner', None)
            if base_id is not None:
                try:
                    base_obj = Base.objects.get(pk=base_id)
                except Base.DoesNotExist:
                    return False
                owner_object = base_obj.child_name
                if request.user.is_superuser:
                    return True
                elif owner_object == 'organization':
                    organization = Organization.objects.get(id=base_obj.id)
                    if organization.owner == request.user:
                        return True
                elif owner_object == 'exchange':
                    exchange = Exchange.objects.get(id=base_obj.id)
                    if exchange.owner.identity_user is not None:
                        if exchange.owner.identity_user == request.user:
                            return True
                    else:
                        if exchange.owner.identity_organization.owner == request.user:
                            return True
                elif owner_object == 'product':
                    product = Product.objects.get(id=base_obj.id)
                    if product.product_user == request.user:
                        return True
                elif owner_object == 'identity':
                    identity = Identity.objects.get(id=base_obj.id)
                    if identity.identity_user is not None:
                        if identity.identity_user == request.user:
                            return True
                    elif identity.identity_organization.owner == request.user:
                        return True
            return False
        return True

    def has_object_permission(self, request, view, obj):

        owner_object = ContentType.objects.get(model=obj.roll_owner.child_name).__str__()
        child_object = getattr(obj.roll_owner, owner_object)

        if request.user.is_superuser:
            return True
        elif owner_object == 'organization':
            if child_object.owner == request.user:
                return True
        elif owner_object == 'exchange':
            if child_object.owner.identity_user is not None:
                if child_object.owner.identity_user == request.user:
                    return True
            else:
                if child_object.owner.identity_organization.owner == request.user:
                    return True
        elif owner_object == 'product':
            if child_object.product_user == request.user:
                return True
        return False


class IsRollPermissionOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            related_roll_id = request.POST.get('roll_permission_related_roll', None)
            base_id = BaseRoll.objects.get(pk=related_roll_id).roll_owner_id
            if base_id is not None:
                try:
                    base_obj = Base.objects.get(pk=base_id)
                except Base.DoesNotExist:
                    return False
                owner_object = base_obj.child_name
                if request.user.is_superuser:
                    return True
                elif owner_object == 'organization':
                    organization = Organization.objects.get(id=base_obj.id)
                    if organization.owner == request.user:
                        return True
                elif owner_object == 'exchange':
                    exchange = Exchange.objects.get(id=base_obj.id)
                    if exchange.owner.identity_user is not None:
                        if exchange.owner.identity_user == request.user:
                            return True
                    else:
                        if exchange.owner.identity_organization.owner == request.user:
                            return True
                elif owner_object == 'product':
                    product = Product.objects.get(id=base_obj.id)
                    if product.product_user == request.user:
                        return True
                elif owner_object == 'identity':
                    identity = Identity.objects.get(id=base_obj.id)
                    if identity.identity_user is not None:
                        if identity.identity_user == request.user:
                            return True
                    elif identity.identity_organization.owner == request.user:
                        return True
            return False
        return True

    def has_object_permission(self, request, view, obj):

        owner_object = ContentType.objects.get(model=obj.roll_permission_related_roll.roll_owner.child_name).__str__()
        child_object = getattr(obj.roll_permission_related_roll.roll_owner, owner_object)

        if request.user.is_superuser:
            return True
        elif owner_object == 'organization':
            if child_object.owner == request.user:
                return True

        elif owner_object == 'exchange':
            if child_object.owner.identity_user is not None:
                if child_object.owner.identity_user == request.user:
                    return True
            else:
                if child_object.owner.identity_organization.owner == request.user:
                    return True
        elif owner_object == 'product':
            if child_object.product_user == request.user:
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


class IsHashtagOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            base_id = request.POST.get('hashtag_base', None)
            if base_id is not None:
                try:
                    base_obj = Base.objects.get(pk=base_id)
                except Base.DoesNotExist:
                    return False
                owner_object = base_obj.child_name
                if request.user.is_superuser:
                    return True
                elif owner_object == 'organization':
                    organization = Organization.objects.get(id=base_obj.id)
                    if organization.owner == request.user:
                        return True
                elif owner_object == 'exchange':
                    exchange = Exchange.objects.get(id=base_obj.id)
                    if exchange.owner.identity_user is not None:
                        if exchange.owner.identity_user == request.user:
                            return True
                    else:
                        if exchange.owner.identity_organization.owner == request.user:
                            return True
                elif owner_object == 'product':
                    product = Product.objects.get(id=base_obj.id)
                    if product.product_user == request.user:
                        return True
                elif owner_object == 'identity':
                    identity = Identity.objects.get(id=base_obj.id)
                    if identity.identity_user is not None:
                        if identity.identity_user == request.user:
                            return True
                    elif identity.identity_organization.owner == request.user:
                        return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        owner_object = ContentType.objects.get(model=obj.hashtag_base.child_name).__str__()
        child_object = getattr(obj.hashtag_base, owner_object)
        if request.user.is_superuser:
            return True
        elif owner_object == 'organization':
            if child_object.owner == request.user:
                return True
        elif owner_object == 'exchange':
            if child_object.owner.identity_user is not None:
                if child_object.owner.identity_user == request.user:
                    return True
            else:
                if child_object.owner.identity_organization.owner == request.user:
                    return True
        elif owner_object == 'product':
            if child_object.product_user == request.user:
                return True
        elif owner_object == 'identity':
            if child_object.identity_user is not None:
                if child_object.identity_user == request.user:
                    return True
            else:
                if child_object.identity_organization.owner == request.user:
                    return True
        return False


class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner_object = ContentType.objects.get(model=obj.comment_parent.child_name).__str__()
        child_object = getattr(obj.comment_parent, owner_object)
        owner_identity = Identity.objects.get(pk=obj.comment_sender)
        # check sender access
        if owner_identity.identity_user is not None:
            if owner_identity.identity_user == request.user:
                return True
        elif owner_identity.identity_organization is not None:
            if owner_identity.identity_organization.owner == request.user:
                return True
        # check parent access
        if request.user.is_superuser:
            return True
        elif owner_object == 'organization':
            if child_object.owner == request.user:
                return True
        elif owner_object == 'exchange':
            if child_object.owner.identity_user is not None:
                if child_object.owner.identity_user == request.user:
                    return True
            else:
                if child_object.owner.identity_organization.owner == request.user:
                    return True
        elif owner_object == 'product':
            if child_object.product_user == request.user:
                return True
        elif owner_object == 'identity':
            if child_object.identity_user is not None:
                if child_object.identity_user == request.user:
                    return True
            else:
                if child_object.identity_organization.owner == request.user:
                    return True
        return False