from graphene import relay, Field, String, Int, ID
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from organizations.models import Organization, StaffCount
from organizations.schemas.queries.staff_count import StaffCountNode
from organizations.forms import StaffCountForm


class CreateStaffCountMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        organization_id = String(required=True)
        count = Int(requeired=True)

    staff_count = Field(StaffCountNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id')
        organization_id = from_global_id(organization_id)[1]
        organization = Organization.objects.get(pk=organization_id)

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        # create staff count
        form = StaffCountForm(input)
        if form.is_valid():
            new_staff_count = form.save(commit=False)
            new_staff_count.organization = organization
            new_staff_count.save()
        else:
            raise Exception(str(form.errors))

        return CreateStaffCountMutation(staff_count=new_staff_count)


class UpdateStaffCountMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        count = Int(requeired=True)

    staff_count = Field(StaffCountNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        staff_count_id = from_global_id(id)[1]
        staff_count = StaffCount.objects.get(pk=staff_count_id)

        if staff_count.organization.user != user:
            raise Exception("Invalid Access to Organization")

        count = input.get('count')

        # update staff count
        form = StaffCountForm(input, instance=staff_count)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateStaffCountMutation(staff_count=staff_count)


class DeleteStaffCountMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        staff_count_id = from_global_id(id)[1]
        staff_count = StaffCount.objects.get(pk=staff_count_id)

        if staff_count.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete staff count
        staff_count.delete()

        return DeleteStaffCountMutation(deleted_id=id)
