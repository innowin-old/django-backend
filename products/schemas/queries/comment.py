from django_filters import OrderingFilter, FilterSet
from graphene_django import DjangoObjectType
from graphene import relay

from products.models import Comment


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'text': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(fields=('id', 'create_time'))


class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (relay.Node,)
