import graphene
from django.contrib.auth.models import User as UserModel
from graphene import ObjectType, AbstractType
from graphene_django import DjangoObjectType

from utils.gravatar import get_gravatar_url


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


class Query(AuthQuery, ObjectType):
    pass


schema = graphene.Schema(query=Query)
