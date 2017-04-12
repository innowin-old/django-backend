from graphene import relay, Field, String
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from media.forms import MediaForm
from media.schemas.queries.media import MediaNode
from users.models import Identity


class CreateMediaMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        identity_id = String(required=True)

    media = Field(MediaNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        identity_id = input.get('identity_id')
        identity_id = from_global_id(identity_id)[1]
        identity = Identity.objects.get(pk=identity_id)

        if not identity.validate_user(user):
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
