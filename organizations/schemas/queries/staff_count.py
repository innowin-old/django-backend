import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay

from organizations.models import StaffCount


class StaffCountFilter(django_filters.FilterSet):

    class Meta:
        model = StaffCount
        fields = {
            'id': ['exact'],
            'count': ['exact', 'gte', 'lte'],
        }

    order_by = OrderingFilter(fields=('id', 'count', 'create_time'))


class StaffCountNode(DjangoObjectType):

    class Meta:
        model = StaffCount
        interfaces = (relay.Node, )
