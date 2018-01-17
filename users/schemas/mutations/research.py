from graphene import relay, Field, List, String, Int, ID

from danesh_boom.viewer_fields import ViewerFields
from users.schemas.queries.research import ResearchNode
from users.models import Research
from users.forms import ResearchForm
from utils.relay_helpers import get_node


class CreateResearchMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        title = String(required=True)
        url = String()
        author = List(String)
        publication = String()
        year = Int()
        page_count = Int()

    research = Field(ResearchNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        # create research
        form = ResearchForm(input)
        if form.is_valid():
            new_research = form.save(commit=False)
            new_research.user = user
            new_research.save()
        else:
            raise Exception(str(form.errors))

        return CreateResearchMutation(research=new_research)


class UpdateResearchMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        title = String(required=True)
        url = String()
        author = List(String)
        publication = String()
        year = Int()
        page_count = Int()

    research = Field(ResearchNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        research_id = input.get('id', None)
        research = get_node(research_id, context, info, Research)

        if not research:
            raise Exception("Invalid Research")

        if research.user != user:
            raise Exception("Invalid Access to Research")

        # update research
        form = ResearchForm(input, instance=research)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateResearchMutation(research=research)


class DeleteResearchMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        research_id = input.get('id', None)
        research = get_node(research_id, context, info, Research)

        if not research:
            raise Exception("Invalid Research")

        if research.user != user:
            raise Exception("Invalid Access to Research")

        # delete research
        research.delete()

        return DeleteResearchMutation(deleted_id=id)
