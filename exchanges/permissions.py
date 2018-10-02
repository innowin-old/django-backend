from django.contrib.auth.models import User
from rest_framework import permissions

from users.models import Identity, AgentRequest
from organizations.models import Organization
from .models import ExchangeIdentity, Exchange


class IsExchangeOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if 'owner' in request.POST:
                identity_id = request.POST.get('owner')
                try:
                    identity = Identity.objects.get(pk=identity_id)
                except Identity.DoesNotExist:
                    return False
                if identity.identity_user is None:
                    try:
                        organization = Organization.objects.get(pk=identity.identity_organization)
                    except Organization.DoesNotExist:
                        return False
                    if organization.owner == request.user or request.user.is_superuser:
                        return True
                    return False
                else:
                    try:
                        user = User.objects.get(pk=identity.identity_user)
                    except User.DoesNotExist:
                        return False
                    if user == request.user or request.user.is_superuser:
                        return True
                return False
            else:
                return True
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        elif obj.owner.identity_organization is None:
            if request.user == obj.owner.identity_user or request.user.is_superuser:
                return True
        elif request.user == obj.owner.identity_organization.owner or request.user.is_superuser:
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
    message = 'exchange is full !'

    def has_permission(self, request, view):
        if request.method == "POST":
            exchange_id = request.POST['exchange_identity_related_exchange']
            if exchange_id is not None:
                try:
                    exchange_obj = Exchange.objects.get(pk=exchange_id)
                except Exchange.DoesNotExist:
                    return False
                exchange_count = ExchangeIdentity.objects.filter(exchange_identity_related_exchange_id=exchange_id,
                                                                 delete_flag=False).count()
                if exchange_count >= exchange_obj.members_count:
                    return False
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == "update":
            active_flag = request.POST.get('active_flag', None)
            if active_flag is not None:
                if obj.active_flag is False and active_flag is True:
                    exchange_count = ExchangeIdentity.objects.filter(
                        exchange_identity_related_exchange=obj.exchange_identity_related_exchange, active_flag=True)
                    if exchange_count < obj.exchange_identity_related_exchange.members_count:
                        return True
                    return False
            return False
        return True


class IsAgentOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if 'owner' in request.POST:
                try:
                    identity = Identity.objects.get(pk=request.POST.get('owner'))
                except Identity.DoesNotExist:
                    return False
            else:
                identity = Identity.objects.get(identity_user=request.user)
            agent = AgentRequest.objects.filter(agent_request_identity=identity)
            if agent.count() != 0:
                return True
            return False
        return True


class IsFirstDefaultExchange(permissions.BasePermission):
    message = "Default Exchange Already Exist"

    def has_permission(self, request, view):
        if request.method == "POST":
            is_default_exchange = request.POST.get('is_default_exchange', None)
            if is_default_exchange is not None:
                default_exchange_count = Exchange.objects.filter(is_default_exchange=True).count()
                if default_exchange_count >= 1:
                    return False
            return True
        return True


class IsJoinedBefore(permissions.BasePermission):
    message = "you joined this exchange before"

    def has_permission(self, request, view):
        if view.action in ['create']:
            exchange_identity_related_identity = request.POST.get('exchange_identity_related_identity', None)
            if exchange_identity_related_identity is None:
                exchange_identity_related_identity = Identity.objects.get(identity_user=request.user).id
            exchange_identity = ExchangeIdentity.objects.filter(
                exchange_identity_related_identity_id=exchange_identity_related_identity,
                exchange_identity_related_exchange_id=request.POST.get('exchange_identity_related_exchange', None),
                delete_flag=False
            )
            if exchange_identity.count() != 0:
                return False
        return True