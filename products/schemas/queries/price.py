from django_filters import OrderingFilter, FilterSet
from graphene_django import DjangoObjectType
from graphene import relay

from products.models import Price


class PriceFilter(FilterSet):
    class Meta:
        model = Price
        fields = {
            'id': ['exact'],
            'value': ['exact', 'gte', 'lte'],
        }

    order_by = OrderingFilter(fields=('id', 'value', 'create_time'))


class PriceNode(DjangoObjectType):
    class Meta:
        model = Price
        interfaces = (relay.Node,)
