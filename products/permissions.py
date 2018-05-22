from rest_framework import permissions
from .models import Product


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