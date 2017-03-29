from graphene import relay, Field, String, Boolean, ID
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from users.schemas.queries.work_experience import WorkExperienceNode
from users.models import WorkExperience
from users.forms import WorkExperienceForm


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
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id', None)
        if organization_id:
            organization_id = from_global_id(organization_id)[1]
            input['organization'] = organization_id

        # create work experience
        form = WorkExperienceForm(input)
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
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        work_experience_id = from_global_id(id)[1]
        work_experience = WorkExperience.objects.get(pk=work_experience_id)
        if work_experience.user != user:
            raise Exception("Invalid Access to Work Experience")

        organization_id = input.get('organization_id', None)
        if organization_id:
            organization_id = from_global_id(organization_id)[1]
            input['organization'] = organization_id

        # update work experience
        form = WorkExperienceForm(input, instance=work_experience)
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
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        work_experience_id = from_global_id(id)[1]
        work_experience = WorkExperience.objects.get(pk=work_experience_id)
        if work_experience.organization.user != user:
            raise Exception("Invalid Access to Work Experience")

        confirm = input.get('confirm')
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
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        work_experience_id = from_global_id(id)[1]
        work_experience = WorkExperience.objects.get(pk=work_experience_id)
        if work_experience.user != user:
            raise Exception("Invalid Access to Work Experience")

        # delete work experience
        work_experience.delete()

        return DeleteWorkExperienceMutation(deleted_id=id)
