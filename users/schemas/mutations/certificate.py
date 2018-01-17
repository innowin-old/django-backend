from graphene import relay, Field, String, ID

from danesh_boom.viewer_fields import ViewerFields
from media.models import Media
from users.forms import CertificateForm
from users.models import Certificate
from users.schemas.queries.certificate import CertificateNode
from utils.relay_helpers import get_node


class CreateCertificateMutation(ViewerFields, relay.ClientIDMutation):
    class Input:
        title = String(required=True)
        picture_id = String()

    certificate = Field(CertificateNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        picture_id = input.get('picture_id')
        picture = get_node(picture_id, context, info, Media)

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
        certificate_id = input.get('id', None)
        certificate = get_node(certificate_id, context, info, Certificate)
        if not certificate:
            raise Exception("Invalid Certificate")

        if certificate.user != user:
            raise Exception("Invalid Access to Certificate")

        picture_id = input.get('picture_id')
        picture = get_node(picture_id, context, info, Media)

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
        certificate_id = input.get('id', None)
        certificate = get_node(certificate_id, context, info, Certificate)
        if not certificate:
            raise Exception("Invalid Certificate")
        if certificate.user != user:
            raise Exception("Invalid Access to Certificate")

        # delete certificate
        certificate.delete()

        return DeleteCertificateMutation(deleted_id=id)
