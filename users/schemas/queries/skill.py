import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay
from django.contrib.postgres.fields import ArrayField

from users.models import Skill


class SkillFilter(django_filters.FilterSet):

    class Meta:
        model = Skill
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'tag': ['icontains'],
            'description': ['exact', 'icontains', 'istartswith'],
        }
        filter_overrides = {
            ArrayField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }

    order_by = OrderingFilter(fields=('id', 'title',))


class SkillNode(DjangoObjectType):

    class Meta:
        model = Skill
        interfaces = (relay.Node, )
