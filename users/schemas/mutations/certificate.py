from graphene import relay, Field, String, ID
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from users.schemas.queries.certificate import CertificateNode
from users.models import Certificate
from users.forms import CertificateForm


class CreateCertificateMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        title = String(required=True)
        picture_id = String()

    certificate = Field(CertificateNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        picture = None
        picture_id = input.get('picture_id')

        if picture_id:
            picture_id = from_global_id(picture_id)[1]
            picture = Media.objects.get(pk=picture_id)

        # create certificate
        form = CertificateForm(input, context.FILES)
        if form.is_valid():
            new_certificate = form.save(commit=False)
            new_certificate.user = user
            new_certificate.picture = picture
            new_certificate.save()
        else:
            raise Exception(str(form.errors))

        return CreateCertificateMutation(certificate=new_certificate)


class UpdateCertificateMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        picture_id = String()
        title = String(required=True)

    certificate = Field(CertificateNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        certificate_id = from_global_id(id)[1]
        certificate = Certificate.objects.get(pk=certificate_id)
        if certificate.user != user:
            raise Exception("Invalid Access to Certificate")

        picture = None
        picture_id = input.get('picture_id')
        if picture_id:
            picture_id = from_global_id(picture_id)[1]
            picture = Media.objects.get(pk=picture_id)

        # update certificate
        certificate.picture = picture
        form = CertificateForm(input, context.FILES, instance=certificate)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateCertificateMutation(certificate=certificate)


class DeleteCertificateMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        certificate_id = from_global_id(id)[1]
        certificate = Certificate.objects.get(pk=certificate_id)
        if certificate.user != user:
            raise Exception("Invalid Access to Work Certificate")

        # delete certificate
        certificate.delete()

        return DeleteCertificateMutation(deleted_id=id)
