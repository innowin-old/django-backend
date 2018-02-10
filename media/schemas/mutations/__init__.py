from graphene import AbstractType

from media.schemas.mutations.media import CreateMediaMutation


class MediaMutation(AbstractType):
    # ---------------- Media ----------------
    create_media = CreateMediaMutation.Field()
