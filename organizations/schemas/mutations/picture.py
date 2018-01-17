from graphene import relay, Field, String, Int, ID

from danesh_boom.viewer_fields import ViewerFields
from organizations.models import Organization, OrganizationPicture
from organizations.schemas.queries.picture import PictureNode
from organizations.forms import PictureForm
from media.models import Media
from utils.relay_helpers import get_node


class CreatePictureMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        organization_id = String(required=True)
        picture_id = String(required=True)
        order = Int(required=True)
        description = String()

    picture = Field(PictureNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id', None)
        organization = get_node(organization_id, context, info, Organization)

        if not organization:
            raise Exception("Invalid Organization")

        if organization.owner != user:
            raise Exception("Invalid Access to Organization")

        media_id = input.get('picture_id')
        media = get_node(media_id, context, info, Media)

        if not media:
            raise Exception("Invalid Media")

        if not media.identity.validate_organization(organization):
            raise Exception("Invalid Media Identiy")

        # create picture
        form = PictureForm(input, context.FILES)
        if form.is_valid():
            new_picture = form.save(commit=False)
            new_picture.organization = organization
            new_picture.picture = media
            new_picture.save()
        else:
            raise Exception(str(form.errors))

        return CreatePictureMutation(picture=new_picture)


class UpdatePictureMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        picture_id = String(required=True)
        order = Int(requeired=True)
        description = String()

    picture = Field(PictureNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        picture_id = input.get('id')
        picture = get_node(picture_id, context, info, Picture)

        if not picture:
            raise Exception("Invalid Picture")

        media_id = input.get('picture_id')
        media = get_node(media_id, context, info, Media)

        if not media:
            raise Exception("Invalid Media")

        if not media.identity.validate_organization(picture.organization):
            raise Exception("Invalid Media Identiy")

        if picture.organization.owner != user:
            raise Exception("Invalid Access to Organization")

        # update picture
        picture.picture = media

        form = PictureForm(input, context.FILES, instance=picture)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdatePictureMutation(picture=picture)


class DeletePictureMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        picture_id = input.get('id')
        picture = get_node(picture_id, context, info, Picture)

        if not picture:
            raise Exception("Invalid Picture")

        if picture.organization.owner != user:
            raise Exception("Invalid Access to Organization")

        # delete picture in media model
        picture.picture.delete()

        # delete picture
        picture.delete()

        return DeletePictureMutation(deleted_id=id)
