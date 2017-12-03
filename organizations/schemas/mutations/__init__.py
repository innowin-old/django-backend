from graphene import AbstractType

from organizations.schemas.mutations.organization import CreateOrganizationMutation, \
    UpdateOrganizationMutation, DeleteOrganizationMutation
from organizations.schemas.mutations.picture import CreatePictureMutation, \
    UpdatePictureMutation, DeletePictureMutation
from organizations.schemas.mutations.staff_count import CreateStaffCountMutation, \
    UpdateStaffCountMutation, DeleteStaffCountMutation


class OrganizationMutation(AbstractType):
    # ---------------- Organization ----------------
    create_organization = CreateOrganizationMutation.Field()
    update_organization = UpdateOrganizationMutation.Field()
    delete_organization = DeleteOrganizationMutation.Field()

    # ---------------- Picture ----------------
    create_organization_picture = CreatePictureMutation.Field()
    update_organization_picture = UpdatePictureMutation.Field()
    delete_organization_picture = DeletePictureMutation.Field()

    # ---------------- StaffCount ----------------
    create_organization_staff_count = CreateStaffCountMutation.Field()
    update_organization_staff_count = UpdateStaffCountMutation.Field()
    delete_organization_staff_count = DeleteStaffCountMutation.Field()
