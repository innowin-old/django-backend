from graphene import relay, AbstractType
from graphene_django.filter import DjangoFilterConnectionField
from organizations.schemas.queries.organization import OrganizationNode, OrganizationFilter


class OrganizationQuery(AbstractType):

    organization = relay.Node.Field(OrganizationNode)
    organizations = DjangoFilterConnectionField(
        OrganizationNode, filterset_class=OrganizationFilter)
