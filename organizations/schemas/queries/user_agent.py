import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay, Field

from organizations.models import UserAgent
from users.schemas.queries.user import UserNode


class UserAgentFilter(django_filters.FilterSet):

    class Meta:
        model = UserAgent
        fields = {
            'id': ['exact'],
            # ---------- Organization ------------
            'organization_id': ['exact'],
            'organization__name': ['exact', 'icontains', 'istartswith'],
            # ---------- User ------------
            'user_id': ['exact'],
            'user__username': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(fields=('id',))


class UserAgentNode(DjangoObjectType):

    user = Field(UserNode)

    class Meta:
        model = UserAgent
        interfaces = (relay.Node, )
