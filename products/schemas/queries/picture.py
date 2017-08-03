from django_filters import OrderingFilter, FilterSet
from graphene_django import DjangoObjectType
from graphene import relay

from products.models import Picture


class ProductPictureFilter(FilterSet):
    class Meta:
        model = Picture
        fields = {
            'id': ['exact'],
        }

    order_by = OrderingFilter(fields=('id', 'order'))


class ProductPictureNode(DjangoObjectType):
    class Meta:
        model = Picture
        interfaces = (relay.Node,)
