import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay

from users.models import Badge


class BadgeFilter(django_filters.FilterSet):

    class Meta:
        model = Badge
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'create_time': ['exact', 'gte', 'lte'],
        }

    order_by = OrderingFilter(fields=('id', 'title', 'create_time'))


class BadgeNode(DjangoObjectType):

    class Meta:
        model = Badge
        interfaces = (relay.Node, )
