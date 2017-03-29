import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay

from users.models import Education


class EducationFilter(django_filters.FilterSet):

    class Meta:
        model = Education
        fields = {
            'grade': ['exact', 'icontains', 'istartswith'],
            'university': ['exact', 'icontains', 'istartswith'],
            'field_of_study': ['exact', 'icontains', 'istartswith'],
            'from_date': ['exact', 'gte', 'lte'],
            'to_date': ['exact', 'gte', 'lte'],
            'average': ['exact', 'gte', 'lte'],
            'description': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(
        fields=(
            'id',
            'grade',
            'university',
            'field_of_study',
            'from_date',
            'to_date',
            'average'))


class EducationNode(DjangoObjectType):

    class Meta:
        model = Education
        interfaces = (relay.Node, )
