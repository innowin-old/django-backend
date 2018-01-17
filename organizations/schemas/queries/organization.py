import django_filters
from django_filters import OrderingFilter
from graphene_django import DjangoObjectType
from graphene import relay, Field, resolve_only_args, String
from django.contrib.postgres.fields import ArrayField
from graphene_django.filter import DjangoFilterConnectionField

from organizations.models import Organization, StaffCount, OrganizationPicture
from organizations.schemas.queries.picture import PictureFilter, PictureNode
from organizations.schemas.queries.staff_count import StaffCountFilter, StaffCountNode
from users.models import WorkExperience
from users.schemas.queries.work_experience import WorkExperienceNode, \
    WorkExperienceFilter
from media.schemas.queries.media import MediaNode


class OrganizationFilter(django_filters.FilterSet):
    class Meta:
        model = Organization
        fields = {
            'id': ['exact'],
            'username': ['exact', 'icontains', 'istartswith'],
            'nike_name': ['exact', 'icontains', 'istartswith'],
            'official_name': ['exact', 'icontains', 'istartswith'],
            'national_code': ['exact', 'icontains', 'istartswith'],
            'registrar_organization': ['exact', 'icontains', 'istartswith'],
            'country': ['exact', 'icontains', 'istartswith'],
            'province': ['exact', 'icontains', 'istartswith'],
            'city': ['exact', 'icontains', 'istartswith'],
            'ownership_type': ['exact'],
            # 'business_type': ['exact'],TODO
            'social_network': ['icontains'],
            'staff_count': ['exact', 'gte', 'lte'],
            # ---------- User ------------
            'owner_id': ['exact'],
            'owner__username': ['exact', 'icontains', 'istartswith'],
            # 'admins__username':[] TODO
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
    OWNERSHIP_TYPES = String()
    BUSINESS_TYPES = String()
    logo = Field(MediaNode)
    organization_staff_counts = DjangoFilterConnectionField(
        StaffCountNode, filterset_class=StaffCountFilter)
    organization_pictures = DjangoFilterConnectionField(
        PictureNode, filterset_class=PictureFilter)
    organization_work_experiences = DjangoFilterConnectionField(
        WorkExperienceNode, filterset_class=WorkExperienceFilter)

    @resolve_only_args
    def resolve_OWNERSHIP_TYPES(self, **args):
        return self.OWNERSHIP_TYPES

    @resolve_only_args
    def resolve_BUSINESS_TYPES(self, **args):
        return self.BUSINESS_TYPES

    @resolve_only_args
    def resolve_logo(self, **args):
        return self.logo

    @resolve_only_args
    def resolve_organization_staff_counts(self, **args):
        staff_counts = StaffCount.objects.filter(organization=self)
        return StaffCountFilter(args, queryset=staff_counts).qs

    @resolve_only_args
    def resolve_organization_pictures(self, **args):
        pictures = OrganizationPicture.objects.filter(organization=self)
        return PictureFilter(args, queryset=pictures).qs

    @resolve_only_args
    def resolve_organization_work_experiences(self, **args):
        work_experiences = WorkExperience.objects.filter(
            organization=self)
        return WorkExperienceFilter(args, queryset=work_experiences).qs

    class Meta:
        model = Organization
        interfaces = (relay.Node,)
        only_fields = [
            'id',
            'username',
            'nike_name',
            'official_name',
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
            'biography',
            'description',
            'correspondence_language',
            'social_network',
            'staff_count',

            'owner',
            'admins',
            'identity',
        ]
