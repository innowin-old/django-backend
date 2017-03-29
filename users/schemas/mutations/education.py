from graphene import relay, Field, String, Float, ID
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from users.schemas.queries.education import EducationNode
from users.models import Education
from users.forms import EducationForm


class CreateEducationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        grade = String(required=True)
        university = String(required=True)
        field_of_study = String(required=True)
        from_date = String()
        to_date = String()
        average = Float()
        description = String()

    education = Field(EducationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        # create research
        form = EducationForm(input)
        if form.is_valid():
            new_education = form.save(commit=False)
            new_education.user = user
            new_education.save()
        else:
            raise Exception(str(form.errors))

        return CreateEducationMutation(education=new_education)


class UpdateEducationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        grade = String(required=True)
        university = String(required=True)
        field_of_study = String(required=True)
        from_date = String()
        to_date = String()
        average = Float()
        description = String()

    education = Field(EducationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        education_id = from_global_id(id)[1]
        education = Education.objects.get(pk=education_id)
        if education.user != user:
            raise Exception("Invalid Access to Education")

        # update education
        form = EducationForm(input, instance=education)
        if form.is_valid():
            education.save()
        else:
            raise Exception(str(form.errors))

        return UpdateEducationMutation(education=education)


class DeleteEducationMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        education_id = from_global_id(id)[1]
        education = Education.objects.get(pk=education_id)
        if education.user != user:
            raise Exception("Invalid Access to Education")

        # delete education
        education.delete()

        return DeleteEducationMutation(deleted_id=id)
