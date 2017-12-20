import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay

from organizations.models import OrganizationPicture


class OrganizationPictureFilter(django_filters.FilterSet):

    class Meta:
        model = OrganizationPicture
        fields = {
            'id': ['exact'],
        }

    order_by = OrderingFilter(fields=('id', 'order'))


class PictureNode(DjangoObjectType):

    class Meta:
        model = OrganizationPicture
        interfaces = (relay.Node, )
