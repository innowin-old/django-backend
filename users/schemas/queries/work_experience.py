import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay

from users.models import WorkExperience 


class WorkExperienceFilter(django_filters.FilterSet):

    class Meta:
        model = WorkExperience
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'position': ['exact', 'icontains', 'istartswith'],
            'from_date': ['exact', 'gte', 'lte'],
            'to_date': ['exact', 'gte', 'lte'],
            'status': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(
        fields=(
            'id',
            'name',
            'position',
            'from_date',
            'to_date',
            'status'))


class WorkExperienceNode(DjangoObjectType):

    class Meta:
        model = WorkExperience
        interfaces = (relay.Node, )
