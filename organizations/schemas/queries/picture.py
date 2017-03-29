import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay

from organizations.models import Picture


class PictureFilter(django_filters.FilterSet):

    class Meta:
        model = Picture
        fields = {
            'id': ['exact'],
        }

    order_by = OrderingFilter(fields=('id', 'order'))


class PictureNode(DjangoObjectType):

    class Meta:
        model = Picture
        interfaces = (relay.Node, )
