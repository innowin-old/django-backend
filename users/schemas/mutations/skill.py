from graphene import relay, Field, List, String, ID
from graphql_relay.node.node import from_global_id

from danesh_boom.viewer_fields import ViewerFields
from users.schemas.queries.skill import SkillNode
from users.models import Skill
from users.forms import SkillForm


class CreateSkillMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        title = String(required=True)
        tag = List(String)
        description = String()

    skill = Field(SkillNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        # create skill
        form = SkillForm(input)
        if form.is_valid():
            new_skill = form.save(commit=False)
            new_skill.user = user
            new_skill.save()
        else:
            raise Exception(str(form.errors))

        return CreateSkillMutation(skill=new_skill)


class UpdateSkillMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        title = String(required=True)
        tag = List(String)
        description = String()

    skill = Field(SkillNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        skill_id = from_global_id(id)[1]
        skill = Skill.objects.get(pk=skill_id)
        if skill.user != user:
            raise Exception("Invalid Access to Skill")

        # update skill
        form = SkillForm(input, instance=skill)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateSkillMutation(skill=skill)


class DeleteSkillMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id', None)
        skill_id = from_global_id(id)[1]
        skill = Skill.objects.get(pk=skill_id)
        if skill.user != user:
            raise Exception("Invalid Access to Skill")

        # delete skill
        skill.delete()

        return DeleteSkillMutation(deleted_id=id)
