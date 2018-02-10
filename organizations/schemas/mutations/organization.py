from graphene import relay, Field, List, String, Int, ID

from danesh_boom.viewer_fields import ViewerFields
from organizations.models import Organization
from organizations.schemas.queries.organization import OrganizationNode
from organizations.forms import OrganizationForm
from media.models import Media
from utils.relay_helpers import get_node
from django.contrib.auth.models import User


def add_admins(organization, input, context, info):
    admins_id = input.get('admins_id', None)
    admins_pk = []
    if admins_id:
        for id in admins_id:
            admin = get_node(id, context, info, User)
            if admin:
                organization.admins.add(admin)
                admins_pk.append(admin.pk)
    for extra_admin in User.objects.filter(organ_admins=organization).exclude(pk__in=admins_pk):
        organization.admins.remove(extra_admin)


class CreateOrganizationMutation(ViewerFields, relay.ClientIDMutation):
    class Input:
        username = String(required=True)
        nike_name = String()
        official_name = String(required=True)
        national_code = String(required=True)
        country = String(required=True)
        province = String(required=True)
        city = String(required=True)
        ownership_type = String(required=True)
        business_type = List(String, required=True)

    organization = Field(OrganizationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):

        user = context.user

        # create organization
        form = OrganizationForm(input)
        if form.is_valid():
            new_organization = form.save(commit=False)
            new_organization.owner = user
            new_organization.save()
        else:
            raise Exception(str(form.errors))

        return CreateOrganizationMutation(organization=new_organization)


class UpdateOrganizationMutation(ViewerFields, relay.ClientIDMutation):
    class Input:
        id = String(required=True)
        admins_id = List(String)
        username = String(required=True)
        nike_name = String()
        official_name = String(required=True)
        national_code = String(required=True)
        registration_ads_url = String()
        registrar_organization = String()
        country = String(required=True)
        province = String(required=True)
        city = String(required=True)
        address = String()
        phone = List(String)
        web_site = String()
        established_year = Int()
        ownership_type = String(required=True)
        business_type = List(String, required=True)
        logo_id = String()
        biography = String()
        description = String()
        correspondence_language = List(String)
        social_network = List(String)
        staff_count = Int()

    organization = Field(OrganizationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('id', None)
        organization = get_node(organization_id, context, info, Organization)

        if not organization:
            raise Exception("Invalid Organization")

        if organization.owner != user:
            raise Exception("Invalid Access to Organization")

        logo_id = input.get('logo_id')
        logo = get_node(logo_id, context, info, Media)

        # update logo
        organization.logo = logo

        # update organization
        form = OrganizationForm(input, instance=organization)
        if form.is_valid():
            add_admins(organization, input, context, info)
            organization.save()
        else:
            raise Exception(str(form.errors))

        return UpdateOrganizationMutation(organization=organization)


class DeleteOrganizationMutation(ViewerFields, relay.ClientIDMutation):
    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('id', None)
        organization = get_node(organization_id, context, info, Organization)

        if not organization:
            raise Exception("Invalid Organization")

        if organization.owner != user:
            raise Exception("Invalid Access to Organization")

        # delete organization
        organization.delete()

        return DeleteOrganizationMutation(deleted_id=id)
