from rest_framework import permissions

from .models import ExchangeIdentity

from django.conf import settings

from users.models import Agent, Identity

from organizations.models import Organization


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
        return True


class IsExchangeFull(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            exchange_id = request.POST['exchange_identity_related_exchange']
            if exchange_id is not None:
                exchange_count = ExchangeIdentity.objects.filter(exchange_identity_related_exchange_id=exchange_id).count()
                if exchange_count > settings.EXCHANGE_LIMIT:
                    return False
        return True


class IsAgentOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            user = request.user
            if 'owner' not in request.POST:
                identity = Identity.objects.get(identity_user=user)
                try:
                    agent = Agent.objects.get(agent_identity=identity)
                except Agent.DoesNotExist:
                    return False
            else:
                if not user.is_superuser:
                    identity = Identity.objects.get(pk=request.POST['owner'])
                    try:
                        agent = Agent.objects.get(agent_identity=identity)
                    except Agent.DoesNotExist:
                        return False
                    if identity.identity_organization:
                        organization = Organization.objects.get(pk=identity.identity_organization)
                        if organization.owner != user:
                            return False
        return True