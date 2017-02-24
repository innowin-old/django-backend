import graphene
from django.contrib.auth.models import User as UserModel
from graphene import ObjectType, AbstractType
from graphene_django import DjangoObjectType

import users.schema
from utils.gravatar import get_gravatar_url

'''
class User(DjangoObjectType):
    avatar = graphene.String()

    class Meta:
        model = UserModel
        only_fields = ('id', 'username', 'first_name', 'last_name', 'avatar')

    def resolve_avatar(self, args, context, info):
        return get_gravatar_url(self.email)


class AuthQuery(AbstractType):
    me = graphene.Field(User)
    def resolve_me(self, args, context, info):
        if not context.user.is_authenticated():
            return None
        return context.user

    users = graphene.List(User)
    @graphene.resolve_only_args
    def resolve_users(self):
        return UserModel.objects.all()
'''


class Query(users.schema.UserQuery, ObjectType):
    pass


class Mutation(users.schema.UserMutation, ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
