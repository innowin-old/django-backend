from rest_framework import permissions

from .models import ExchangeIdentity


class IsExchangeOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        elif request.user == obj.owner.identity_user or request.user.is_superuser:
            return True
        return False


class IsExchangeIdentity(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.exchange_identity_related_exchange.owner.identity_user:
            return True
        return False

    def has_permission(self, request, view):
        exchange = request.query_params.get('exchange')
        if exchange is not None:
            get_user_exchange = ExchangeIdentity.objects.filter(exchange_identity_related_exchange=exchange,
                                                                exchange_identity_related_identity__identity_user=request.user
                                                                )
            if get_user_exchange.count() != 0 or request.user.is_superuser:
                return True
        return False
