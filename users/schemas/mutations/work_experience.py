from graphene import relay, Field, String, Boolean, ID

from danesh_boom.viewer_fields import ViewerFields
from organizations.models import Organization
from users.forms import WorkExperienceForm
from users.models import WorkExperience
from users.schemas.queries.work_experience import WorkExperienceNode
from utils.relay_helpers import get_node


class CreateWorkExperienceMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        name = String()
        organization_id = String()
        position = String(required=True)
        from_date = String()
        to_date = String()
        status = String()

    work_experience = Field(WorkExperienceNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        user = context.user
        organization_id = args.get('organization_id', None)
        organization = get_node(organization_id, context, info, Organization)
        if organization:
            args['organization'] = organization.id

        # create work experience
        form = WorkExperienceForm(args)
        if form.is_valid():
            new_work_experience = form.save(commit=False)
            new_work_experience.user = user
            new_work_experience.save()
        else:
            raise Exception(str(form.errors))

        return CreateWorkExperienceMutation(
            work_experience=new_work_experience
        )


class UpdateWorkExperienceMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        name = String()
        organization_id = String()
        position = String(required=True)
        from_date = String()
        to_date = String()
        status = String()

    work_experience = Field(WorkExperienceNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        user = context.user
        work_experience_id = args.get('id', None)
        work_experience = get_node(
            work_experience_id, context, info, WorkExperience)

        if not work_experience:
            raise Exception("Invalid Work Experience id")

        if work_experience.user != user:
            raise Exception("Invalid Access to Work Experience")

        organization_id = args.get('organization_id', None)
        organization = get_node(organization_id, context, info, Organization)
        if organization:
            args['organization'] = organization.id

        # update work experience
        form = WorkExperienceForm(args, instance=work_experience)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateWorkExperienceMutation(work_experience=work_experience)


class ConfirmWorkExperienceMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        confirm = Boolean(required=True)

    work_experience = Field(WorkExperienceNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        user = context.user
        work_experience_id = args.get('id', None)
        work_experience = get_node(
            work_experience_id, context, info, WorkExperience)

        if not work_experience:
            raise Exception("Invalid Work Experience id")

        if work_experience.organization.user != user:
            raise Exception("Invalid Access to Work Experience")

        confirm = args.get('confirm')
        if confirm:
            work_experience.status = 'CONFIRMED'
        else:
            work_experience.status = 'UNCONFIRMED'
        work_experience.save()

        return ConfirmWorkExperienceMutation(work_experience=work_experience)


class DeleteWorkExperienceMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        user = context.user
        work_experience_id = args.get('id', None)
        work_experience = get_node(
            work_experience_id, context, info, WorkExperience)

        if not work_experience:
            raise Exception("Invalid Work Experience")

        if work_experience.user != user:
            raise Exception("Invalid Access to Work Experience")

        # delete work experience
        work_experience.delete()

        return DeleteWorkExperienceMutation(deleted_id=id)
