from graphene import relay, Field, String, ID
from graphql_relay.node.node import from_global_id
from django.contrib.auth.models import User

from danesh_boom.viewer_fields import ViewerFields
from organizations.models import Organization, UserAgent
from organizations.schemas.queries.user_agent import UserAgentNode
from organizations.forms import UserAgentForm


class CreateUserAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        organization_id = String(required=True)
        user_id = String(required=True)
        agent_subject = String()

    user_agent = Field(UserAgentNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        organization_id = input.get('organization_id')
        organization_id = from_global_id(organization_id)[1]
        organization = Organization.objects.get(pk=organization_id)

        user_agent_id = input.get('user_id')
        user_agent_id = from_global_id(user_agent_id)[1]
        user_agent = User.objects.get(pk=user_agent_id)

        if organization.user != user:
            raise Exception("Invalid Access to Organization")

        # TODO check business logic
        if organization.user == user_agent:
            raise Exception("Organization Owner cant not be Agent")

        # create user agent
        form = UserAgentForm(input)
        if form.is_valid():
            new_user_agent = form.save(commit=False)
            new_user_agent.organization = organization
            new_user_agent.user = user_agent
            new_user_agent.save()
        else:
            raise Exception(str(form.errors))

        return CreateUserAgentMutation(user_agent=new_user_agent)


class UpdateUserAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        agent_subject = String()

    user_agent = Field(UserAgentNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        user_agent_id = from_global_id(id)[1]
        user_agent = UserAgent.objects.get(pk=user_agent_id)

        if user_agent.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # update agent
        form = UserAgentForm(input, instance=user_agent)
        if form.is_valid():
            form.save()
        else:
            raise Exception(str(form.errors))

        return UpdateUserAgentMutation(user_agent=user_agent)


class DeleteUserAgentMutation(ViewerFields, relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user
        id = input.get('id')
        user_agent_id = from_global_id(id)[1]
        user_agent = UserAgent.objects.get(pk=user_agent_id)

        if user_agent.organization.user != user:
            raise Exception("Invalid Access to Organization")

        # delete user agent
        user_agent.delete()

        return DeleteUserAgentMutation(deleted_id=id)
