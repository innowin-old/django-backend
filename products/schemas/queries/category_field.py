from django_filters import OrderingFilter, FilterSet
from graphene_django import DjangoObjectType
from graphene import relay
from products.models import CategoryField


class CategoryFieldFilter(FilterSet):
    class Meta:
        model = CategoryField
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'title': ['exact', 'icontains', 'istartswith'],
            'type': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(
        fields=('id', 'order', 'name', 'type'))


class CategoryFieldNode(DjangoObjectType):
    class Meta:
        model = CategoryField
        interfaces = (relay.Node,)
