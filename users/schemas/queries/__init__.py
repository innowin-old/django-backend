from graphene import relay, AbstractType, Field
from graphene_django.filter import DjangoFilterConnectionField
from users.schemas.queries.user import UserFilter, UserNode

from organizations.models import Organization


class UserQuery(AbstractType):
    me = Field(UserNode)

    def resolve_me(self, args, context, info):
        if not context.user.is_authenticated():
            return None
        return context.user
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)
