import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay

from users.models import Certificate


class CertificateFilter(django_filters.FilterSet):

    class Meta:
        model = Certificate
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(
        fields=('id', 'title'))


class CertificateNode(DjangoObjectType):

    class Meta:
        model = Certificate
        interfaces = (relay.Node, )
