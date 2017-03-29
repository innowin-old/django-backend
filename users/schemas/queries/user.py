import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay, resolve_only_args, String
from django.contrib.auth.models import User
from graphene_django.filter import DjangoFilterConnectionField

from users.models import Profile, Education, Research, Certificate,\
    WorkExperience, Skill, Badge
from users.schemas.queries.skill import SkillFilter, SkillNode
from users.schemas.queries.work_experience import WorkExperienceFilter,\
    WorkExperienceNode
from users.schemas.queries.certificate import CertificateFilter, CertificateNode
from users.schemas.queries.research import ResearchFilter, ResearchNode
from users.schemas.queries.education import EducationFilter, EducationNode
from users.schemas.queries.badge import BadgeFilter, BadgeNode
from media.schemas.queries.media import MediaFilter, MediaNode
from utils.gravatar import get_gravatar_url


class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = {
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

    order_by = OrderingFilter(fields=('id', 'date_joined', 'username',))


class UserNode(DjangoObjectType):
    avatar = String()
    user_skills = DjangoFilterConnectionField(
        SkillNode, filterset_class=SkillFilter)
    user_work_experiences = DjangoFilterConnectionField(
        WorkExperienceNode, filterset_class=WorkExperienceFilter)
    user_certificates = DjangoFilterConnectionField(
        CertificateNode, filterset_class=CertificateFilter)
    user_researches = DjangoFilterConnectionField(
        ResearchNode, filterset_class=ResearchFilter)
    user_educations = DjangoFilterConnectionField(
        EducationNode, filterset_class=EducationFilter)
    user_badges = DjangoFilterConnectionField(
        BadgeNode, filterset_class=BadgeFilter)
    user_medias = DjangoFilterConnectionField(
        MediaNode, filterset_class=MediaFilter)

    @resolve_only_args
    def resolve_user_skills(self, **args):
        skills = Skill.objects.filter(user=self)
        return SkillFilter(args, queryset=skills).qs

    @resolve_only_args
    def resolve_user_work_experiences(self, **args):
        work_experiences = WorkExperience.objects.filter(user=self)
        return WorkExperienceFilter(args, queryset=work_experiences).qs

    @resolve_only_args
    def resolve_user_certificates(self, **args):
        certificates = Certificate.objects.filter(user=self)
        return CertificateFilter(args, queryset=certificates).qs

    @resolve_only_args
    def resolve_user_researches(self, **args):
        researches = Research.objects.filter(user=self)
        return ResearchFilter(args, queryset=researches).qs

    @resolve_only_args
    def resolve_user_educations(self, **args):
        educations = Education.objects.filter(user=self)
        return EducationFilter(args, queryset=educations).qs

    @resolve_only_args
    def resolve_user_badges(self, **args):
        badges = Badge.objects.filter(user=self)
        return BadgeFilter(args, queryset=badges).qs

    @resolve_only_args
    def resolve_user_medias(self, **args):
        medias = Media.objects.filter(uploader=self)
        return MediaFilter(args, queryset=medias).qs

    class Meta:
        model = User
        interfaces = (relay.Node, )
        only_fields = ['id', 'username', 'first_name', 'last_name',
                       'date_joined', 'profile', 'educations']

    def resolve_avatar(self, args, context, info):
        return get_gravatar_url(self.email)


class ProfileNode(DjangoObjectType):

    class Meta:
        model = Profile
        interfaces = (relay.Node, )
