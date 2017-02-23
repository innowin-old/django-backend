from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from graphene import relay, String, Field, ObjectType, AbstractType
from graphene_django.filter import DjangoFilterConnectionField

from utils.gravatar import get_gravatar_url
from users.models import Profile, Education, Research, Certificate,\
    WorkExperience, Skill


class SkillNode(DjangoObjectType):

    class Meta:
        model = Skill
        interfaces = (relay.Node, )


class WorkExperienceNode(DjangoObjectType):

    class Meta:
        model = WorkExperience
        interfaces = (relay.Node, )


class CertificateNode(DjangoObjectType):

    class Meta:
        model = Certificate
        interfaces = (relay.Node, )


class ResearchNode(DjangoObjectType):

    class Meta:
        model = Research
        interfaces = (relay.Node, )


class EducationNode(DjangoObjectType):

    class Meta:
        model = Education
        interfaces = (relay.Node, )


class ProfileNode(DjangoObjectType):

    class Meta:
        model = Profile
        interfaces = (relay.Node, )


class UserNode(DjangoObjectType):
    avatar = String()

    class Meta:
        model = User
        interfaces = (relay.Node, )
        filter_fields = {
            'id': ['exact'],
            'username': ['exact', 'icontains', 'istartswith'],
            'first_name': ['exact', 'icontains', 'istartswith'],
            'last_name': ['exact', 'icontains', 'istartswith'],
            'date_joined': ['exact', 'gte', 'lte'],
            # ---------- Profile ------------
            'profile__public_email': ['exact', 'icontains',
                                      'istartswith'],
            'profile__national_code': ['exact', 'icontains',
                                       'istartswith'],
        }
        only_fields = ['id', 'username', 'first_name', 'last_name',
                       'date_joined', 'profile', 'educations',
                       'researches', 'certificates', 'skills',
                       'work_experiences']

    def resolve_avatar(self, args, context, info):
        return get_gravatar_url(self.email)


class UserQuery(AbstractType):
    me = Field(UserNode)

    def resolve_me(self, args, context, info):
        if not context.user.is_authenticated():
            return None
        return context.user
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)
