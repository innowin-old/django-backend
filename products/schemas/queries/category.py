from django_filters import OrderingFilter, FilterSet
from graphene_django import DjangoObjectType
from graphene import relay

from products.models import Category


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'title': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(fields=('id', 'name', 'title'))


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (relay.Node,)
