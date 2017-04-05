import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay, Field, resolve_only_args
from django.contrib.postgres.fields import ArrayField
from graphene_django.filter import DjangoFilterConnectionField

from organizations.models import Organization, StaffCount, Picture,\
    UserAgent
from organizations.schemas.queries.user_agent import UserAgentFilter, UserAgentNode
from organizations.schemas.queries.picture import PictureFilter, PictureNode
from organizations.schemas.queries.staff_count import StaffCountFilter, StaffCountNode
from users.models import WorkExperience
from users.schemas.queries.work_experience import WorkExperienceNode,\
    WorkExperienceFilter
from media.schemas.queries.media import MediaNode


class OrganizationFilter(django_filters.FilterSet):

    class Meta:
        model = Organization
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'organ_name': ['exact', 'icontains', 'istartswith'],
            'national_code': ['exact', 'icontains', 'istartswith'],
            'registrar_organization': ['exact', 'icontains', 'istartswith'],
            'country': ['exact', 'icontains', 'istartswith'],
            'province': ['exact', 'icontains', 'istartswith'],
            'city': ['exact', 'icontains', 'istartswith'],
            'ownership_type': ['exact', 'icontains', 'istartswith'],
            'business_type': ['icontains'],
            # ---------- User ------------
            'user_id': ['exact'],
            'user__username': ['exact', 'icontains', 'istartswith'],
        }
        filter_overrides = {
            ArrayField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }

    order_by = OrderingFilter(fields=('id', 'established_year',))


class OrganizationNode(DjangoObjectType):

    logo = Field(MediaNode)
    organization_staff_counts = DjangoFilterConnectionField(
        StaffCountNode, filterset_class=StaffCountFilter)
    organization_pictures = DjangoFilterConnectionField(
        PictureNode, filterset_class=PictureFilter)
    organization_user_agents = DjangoFilterConnectionField(
        UserAgentNode, filterset_class=UserAgentFilter)
    organization_work_experiences = DjangoFilterConnectionField(
        WorkExperienceNode, filterset_class=WorkExperienceFilter)

    @resolve_only_args
    def resolve_logo(self, **args):
        return self.logo

    @resolve_only_args
    def resolve_organization_staff_counts(self, **args):
        staff_counts = StaffCount.objects.filter(organization=self)
        return StaffCountFilter(args, queryset=staff_counts).qs

    @resolve_only_args
    def resolve_organization_pictures(self, **args):
        pictures = Picture.objects.filter(organization=self)
        return PictureFilter(args, queryset=pictures).qs

    @resolve_only_args
    def resolve_organization_user_agents(self, **args):
        user_agents = UserAgent.objects.filter(organization=self)
        return UserAgentFilter(args, queryset=user_agents).qs

    @resolve_only_args
    def resolve_organization_work_experiences(self, **args):
        work_experiences = WorkExperience.objects.filter(
            organization=self)
        return WorkExperienceFilter(args, queryset=work_experiences).qs

    class Meta:
        model = Organization
        interfaces = (relay.Node, )
        only_fields = [
            'id',
            'name',
            'organ_name',
            'national_code',
            'phone',
            'registration_ads_url',
            'registrar_organization',
            'country',
            'province',
            'city',
            'address',
            'web_site',
            'established_year',
            'ownership_type',
            'business_type',
            'description',
            'advantages',
            'correspondence_language',
        ]
