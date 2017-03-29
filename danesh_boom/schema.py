import graphene
from graphene import ObjectType

from media.schemas.queries import MediaQuery
from media.schemas.mutations import MediaMutation
from organizations.schemas.queries import OrganizationQuery
from organizations.schemas.mutations import OrganizationMutation
from users.schemas.queries import UserQuery
from users.schemas.mutations import UserMutation
from danesh_boom.viewer_fields import ViewerFields


class ViewerNode(
        UserQuery,
        OrganizationQuery,
        MediaQuery,
        ObjectType):

    class Meta:
        interfaces = (graphene.relay.Node,)

    @classmethod
    def get_node(cls, id, context, info):
        if id == "0":
            return ViewerNode(id=id)
        return None


class Query(ViewerFields, ObjectType):
    pass


class Mutation(
        UserMutation,
        OrganizationMutation,
        MediaMutation,
        ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
