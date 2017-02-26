import graphene
from graphene import ObjectType

import users.schema


class Query(users.schema.UserQuery, ObjectType):
    pass


class Mutation(users.schema.UserMutation, ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
