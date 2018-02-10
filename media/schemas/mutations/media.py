from graphene import relay, Field, String

from danesh_boom.viewer_fields import ViewerFields
from media.forms import MediaForm
from media.schemas.queries.media import MediaNode
from users.models import Identity
from utils.relay_helpers import get_node


class CreateMediaMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        identity_id = String(required=True)

    media = Field(MediaNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        identity_id = input.get('identity_id')
        identity = get_node(identity_id, context, info, Identity)

        if not identity or not identity.validate_user(user):
            raise Exception("Invalid Identity")

        if not 'file' in context.FILES:
            raise Exception("File Does Not Exists")

        if not context.user.is_authenticated():
            raise Exception("Login required")

        media_form = MediaForm(
            {'uploader': user.pk},
            context.FILES
        )

        if media_form.is_valid():
            media = media_form.save(commit=False)
            media.identity = identity
            media.save()
        else:
            raise Exception(str(media_form.errors))

        return CreateMediaMutation(media=media)
