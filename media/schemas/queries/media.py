import django_filters
from django_filters import OrderingFilter
from graphene import String
from graphene import resolve_only_args
from graphene_django import DjangoObjectType
from graphene import relay

from media.models import Media


class MediaFilter(django_filters.FilterSet):
    class Meta:
        model = Media
        fields = {
            'id': ['exact'],
            'create_time': ['exact', 'gte', 'lte'],
            # ---------- Uploader ------------
            'uploader_id': ['exact'],
            'uploader__username': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(fields=('id', 'order', 'create_time'))


class MediaNode(DjangoObjectType):
    url = String()

    class Meta:
        model = Media
        interfaces = (relay.Node,)
        exclude_fields = ['file']

    @resolve_only_args
    def resolve_url(self, **args):
        print(self)
        return self.file.url
