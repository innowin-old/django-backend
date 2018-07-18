from rest_framework import permissions
from .models import Product
from users.models import Identity


class IsPriceProductOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        try:
            product_id = int(request.POST['price_product'])
        except ValueError:
            return False
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return False
        if product.product_user == request.user or request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if obj.price_product.product_user == request.user or request.user.is_superuser:
            return True
        return False


class IsPictureProductOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            product_id = request.POST.get('picture_product')
            if product_id.isdigit():
                try:
                    product = Product.objects.get(pk=product_id)
                except Product.DoesNotExist:
                    return False
                if product.product_user == request.user or request.user.is_superuser:
                    return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            if obj.picture_product.product_user == request.user or request.user.is_superuser:
                return True
            return False
        return True


class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            if obj.comment_user == request.user or obj.comment_product.owner == request.user or request.user.is_superuser:
                return True
            return False
        return True


class IsProductOrganizationOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            owner_id = request.POST.get('product_owner', None)
            try:
                identity = Identity.objects.get(pk=owner_id)
            except Identity.DoesNotExist:
                return False
            if identity.identity_user is not None:
                if identity.identity_user == request.user or request.user.is_superuser:
                    return True
            else:
                if identity.identity_organization.owner == request.user or request.user.is_superuser:
                    return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method != "GET":
            try:
                identity = Identity.objects.get(id=obj.product_owner_id)
            except Identity.DoesNotExist:
                return False
            if identity.identity_user is not None:
                if identity.identity_user == request.user or request.user.is_superuser:
                    return True
            else:
                if identity.identity_organization.owner == request.user or request.user.is_superuser:
                    return True
            return False
        return True