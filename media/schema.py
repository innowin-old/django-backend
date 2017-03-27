import django_filters
from django_filters import OrderingFilter
from graphene import AbstractType
from graphene import relay, Field
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from danesh_boom.viewer_fields import ViewerFields
from media.forms import MediaForm
from media.models import Media


#################### Media #######################

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

    class Meta:
        model = Media
        interfaces = (relay.Node,)


class CreateMediaMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        pass

    media = Field(MediaNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        if not 'file' in context.FILES:
            raise Exception("File Does Not Exists")

        if not context.user.is_authenticated():
            raise Exception("Login required")

        media_form = MediaForm(
            {'uploader': user.pk},
            context.FILES
        )

        if media_form.is_valid():
            media = media_form.save()
        else:
            raise Exception(str(media_form.errors))

        return CreateMediaMutation(media=media)


#################### Media Query & Mutation #######################

class MediaQuery(AbstractType):
    media = relay.Node.Field(MediaNode)
    medias = DjangoFilterConnectionField(
        MediaNode, filterset_class=MediaFilter)


class MediaMutation(AbstractType):
    # ---------------- Media ----------------
    create_media = CreateMediaMutation.Field()
