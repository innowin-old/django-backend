from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene import AbstractType

from media.schemas.queries.media import MediaFilter, MediaNode


class MediaQuery(AbstractType):
    media = relay.Node.Field(MediaNode)
    medias = DjangoFilterConnectionField(
        MediaNode, filterset_class=MediaFilter)
