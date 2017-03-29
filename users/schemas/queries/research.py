import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay
from django.contrib.postgres.fields import ArrayField

from users.models import Research


class ResearchFilter(django_filters.FilterSet):

    class Meta:
        model = Research
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'publication': ['exact', 'icontains', 'istartswith'],
            'author': ['icontains'],
            'year': ['exact', 'gte', 'lte'],
            'page_count': ['exact', 'gte', 'lte'],
        }
        filter_overrides = {
            ArrayField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }

    order_by = OrderingFilter(
        fields=(
            'id',
            'title',
            'publication',
            'year',
            'page_count'))


class ResearchNode(DjangoObjectType):

    class Meta:
        model = Research
        interfaces = (relay.Node, )
