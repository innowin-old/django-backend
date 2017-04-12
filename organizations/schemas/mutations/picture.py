from graphene import relay, Field, String, Int, ID
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from organizations.models import Organization, Picture
from organizations.schemas.queries.picture import PictureNode
from organizations.forms import PictureForm
from media.models import Media


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
        organization_id = input.get('organization_id')
        organization_id = from_global_id(organization_id)[1]
        organization = Organization.objects.get(pk=organization_id)

        media_id = input.get('picture_id')
        media_id = from_global_id(media_id)[1]
        media = Media.objects.get(pk=media_id)

        if not media.identity.validate_organization(organization):
            raise Exception("Invalid Media Identiy")

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

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
        id = input.get('id')
        picture_id = from_global_id(id)[1]
        picture = Picture.objects.get(pk=picture_id)

        media_id = input.get('picture_id')
        media_id = from_global_id(media_id)[1]
        picture_media = Media.objects.get(pk=media_id)

        if not picture_media.identity.validate_organization(
                picture.organization):
            raise Exception("Invalid Media Identiy")

        if picture.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # update picture
        picture.picture = picture_media

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
        id = input.get('id')
        picture_id = from_global_id(id)[1]
        picture = Picture.objects.get(pk=picture_id)

        if picture.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete picture in media model
        picture.picture.delete()

        # delete picture
        picture.delete()

        return DeletePictureMutation(deleted_id=id)
