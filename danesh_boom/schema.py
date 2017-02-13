import graphene
from django.contrib.auth.models import User
from graphene import ObjectType, AbstractType
from graphene_django import DjangoObjectType


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'username', 'first_name', 'last_name')


class AuthQuery(AbstractType):
    me = graphene.Field(UserNode)

    def resolve_me(self, args, context, info):
        if not context.user.is_authenticated():
            return None
        return context.user


class Query(AuthQuery, ObjectType):
    pass


schema = graphene.Schema(query=Query)
