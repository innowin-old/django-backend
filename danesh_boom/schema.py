import graphene
from graphene import ObjectType

import users.schema
from danesh_boom.viewer_fields import ViewerFields


class ViewerNode(users.schema.UserQuery, ObjectType):

    class Meta:
        interfaces = (graphene.relay.Node,)

    @classmethod
    def get_node(cls, id, context, info):
        if id == "0":
            return ViewerNode(id=id)
        return None


class Query(ViewerFields, ObjectType):
    pass


class Mutation(users.schema.UserMutation, ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
