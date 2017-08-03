from django_filters import OrderingFilter, FilterSet
from graphene_django import DjangoObjectType
from graphene import relay

from products.models import Price


class PriceFilter(FilterSet):
    class Meta:
        model = Price
        fields = {
            'id': ['exact'],
            'price': ['exact', 'gte', 'lte'],
            'create_time': ['exact', 'gte', 'lte'],
        }

    order_by = OrderingFilter(fields=('id', 'price', 'create_time'))


class PriceNode(DjangoObjectType):
    class Meta:
        model = Price
        interfaces = (relay.Node,)
