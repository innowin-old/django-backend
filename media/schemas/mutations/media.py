from graphene import relay, Field
from danesh_boom.viewer_fields import ViewerFields

from media.forms import MediaForm
from media.models import Media
from media.schemas.queries.media import MediaNode


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
