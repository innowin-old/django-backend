from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import list_route
from rest_framework.response import Response

import json

from base.permissions import IsOwnerOrReadOnly
from base.views import BaseModelViewSet
from .permissions import (
    StaffOrganizationOwner,
    StaffCountOrganizationOwner,
    PictureOrganizationOwner,
    FollowOwner,
    CustomerOrganizationOwner,
    ConfirmationOwner
)

from .models import (
    Organization,
    StaffCount,
    OrganizationPicture,
    Staff,
    Follow,
    Ability,
    Confirmation,
    Customer,
    MetaData
)

from .serializers import (
    OrganizationSerializer,
    OrganizationListViewSerializer,
    StaffCountSerializer,
    OrganizationPictureSerializer,
    StaffSerializer,
    StaffListViewSerializer,
    FollowSerializer,
    AbilitySerializer,
    ConfirmationSerializer,
    ConfirmationListViewSerializer,
    CustomerSerializer,
    MetaDataSerializer
)


class OrganizationViewset(BaseModelViewSet):
    owner_field = 'owner'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Organization.objects.filter(delete_flag=False)

        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner_id=owner)

        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username__contains=username)

        nike_name = self.request.query_params.get('nike_name', None)
        if nike_name is not None:
            queryset = queryset.filter(nike_name__contains=nike_name)

        official_name = self.request.query_params.get('official_name', None)
        if official_name is not None:
            queryset = queryset.filter(official_name__contains=official_name)

        national_code = self.request.query_params.get('national_code', None)
        if national_code is not None:
            queryset = queryset.filter(national_code=national_code)

        registration_ads_url = self.request.query_params.get('registration_ads_url', None)
        if registration_ads_url is not None:
            queryset = queryset.filter(registration_ads_url=registration_ads_url)

        registrar_organization = self.request.query_params.get('registrar_organization', None)
        if registrar_organization is not None:
            queryset = queryset.filter(registrar_organization__contains=registrar_organization)

        country = self.request.query_params.get('country', None)
        if country is not None:
            queryset = queryset.filter(country=country)

        province = self.request.query_params.get('province', None)
        if province is not None:
            queryset = queryset.filter(province=province)

        city = self.request.query_params.get('city', None)
        if city is not None:
            queryset = queryset.filter(city=city)

        address = self.request.query_params.get('address', None)
        if address is not None:
            queryset = queryset.filter(address=address)

        phone = self.request.query_params.get('phone', None)
        if phone is not None:
            queryset = queryset.filter(phone=phone)

        web_site = self.request.query_params.get('web_site', None)
        if web_site is not None:
            queryset = queryset.filter(web_site=web_site)

        established_year = self.request.query_params.get('established_year', None)
        if established_year is not None:
            queryset = queryset.filter(established_year=established_year)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return OrganizationListViewSerializer
        return OrganizationSerializer

    @list_route(
        permission_classes=[AllowAny],
        methods=['post'])
    def import_organizations(self, request):
        jsonString = request.data.get('records', None)
        data = json.loads(jsonString)
        errors = []
        for record in data:
            try:
                organization = Organization.objects.create(
                    username=record.get('username', None),
                    email=record.get('email', None),
                    nike_name=record.get('nike_name', None),
                    official_name=record.get('official_name', None),
                    national_code=record.get('national_code', None),
                    registration_ads_url=record.get('registration_ads_url', None),
                    country=record.get('country', None),
                    province=record.get('province', None),
                    city=record.get('city', None),
                    address=record.get('address', None),
                    phone=record.get('phone', None),
                    web_site=record.get('web_site', None),
                    established_year=record.get('established_year', None),
                    business_type=record.get('business_type', None),
                    biography=record.get('biography'),
                    description=record.get('description'),
                    correspondence_language=record.get('correspondence_language', None),
                    social_network=record.get('social_network', None),
                    owner=record.get('owner', None),
                    organization_logo=record.get('organization_logo', None),
                    admins=record.get('admins', None)
                )
            except Exception as e:
                errors.append({
                    'data': record,
                    'status': str(e)
                })
        response = {
            'errors': errors
        }
        return Response(response)


class StaffCountViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, StaffCountOrganizationOwner]

    def get_queryset(self):
        queryset = StaffCount.objects.filter(delete_flag=False)

        organization_id = self.request.query_params.get('organization_id', None)
        if organization_id is not None:
            queryset = queryset.filter(staff_count_organization_id=organization_id)

        organization_nike_name = self.request.query_params.get('organization_nike_name')
        if organization_nike_name is not None:
            queryset = queryset.filter(staff_count_organization__nike_name__contains=organization_nike_name)

        organization_username = self.request.query_params.get('organization_username')
        if organization_username is not None:
            queryset = queryset.filter(staff_count_organization__username__contains=organization_username)

        return queryset

    def get_serializer_class(self):
        return StaffCountSerializer


class OrganizationPictureViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, PictureOrganizationOwner]

    def get_queryset(self):
        queryset = OrganizationPicture.objects.filter(delete_flag=False)

        organization_id = self.request.query_params.get('organization_id', None)
        if organization_id is not None:
            queryset = queryset.filter(picture_organization_id=organization_id)

        organization_nike_name = self.request.query_params.get('organization_nike_name')
        if organization_nike_name is not None:
            queryset = queryset.filter(staff_count_organization__nike_name__contains=organization_nike_name)

        organization_username = self.request.query_params.get('organization_username')
        if organization_username is not None:
            queryset = queryset.filter(staff_count_organization__username__contains=organization_username)

        return queryset

    def get_serializer_class(self):
        return OrganizationPictureSerializer


class StaffViewset(BaseModelViewSet):
    # queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated, StaffOrganizationOwner]

    def get_queryset(self):
        queryset = Staff.objects.filter(delete_flag=False)

        """
            Organizations Filter Options
        """
        organization_id = self.request.query_params.get('organization_id', None)
        if organization_id is not None:
            queryset = queryset.filter(staff_organization_id=organization_id)

        organization_username = self.request.query_params.get('organization_username', None)
        if organization_username is not None:
            queryset = queryset.filter(staff_organization__username__contains=organization_username)

        organization_official_name = self.request.query_params.get('organization_official_name', None)
        if organization_official_name is not None:
            queryset = queryset.filter(staff_organization__official_name__contains=organization_official_name)

        organization_nike_name = self.request.query_params.get('organization_nike_name', None)
        if organization_official_name is not None:
            queryset = queryset.filter(staff_organization__nike_name__contains=organization_nike_name)

        """
            Users Filter Options
        """
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(staff_user_id=user_id)

        user_username = self.request.query_params.get('user_username', None)
        if user_username is not None:
            queryset = queryset.filter(staff_user__username__contains=user_username)

        user_email = self.request.query_params.get('user_email', None)
        if user_email is not None:
            queryset = queryset.filter(staff_user__email=user_email)

        position = self.request.query_params.get('position', None)
        if position is not None:
            queryset = queryset.filter(position=position)

        post_permission = self.request.query_params.get('post_permission', None)
        if post_permission is not None:
            queryset = queryset.filter(post_permission=post_permission)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return StaffListViewSerializer
        return StaffSerializer


class FollowViewset(BaseModelViewSet):
    # queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated, FollowOwner]

    def get_queryset(self):
        queryset = Follow.objects.filter(delete_flag=False)

        """
            Identity Filter Options
        """
        identity_id = self.request.query_params.get('identity_id', None)
        if identity_id is not None:
            queryset = queryset.filter(follow_identity_id=identity_id)

        identity_name = self.request.query_params.get('identity_name', None)
        if identity_name is not None:
            queryset = queryset.filter(follow_identity__name__contains=identity_name)

        identity_user_username = self.request.query_params.get('identity_user_username', None)
        if identity_user_username is not None:
            queryset = queryset.filter(follow_identity__identity_user__username__contains=identity_user_username)

        """
            Follower Filter Options
        """
        follower_id = self.request.query_params.get('follower_id', None)
        if follower_id is not None:
            queryset = queryset.filter(follow_follower_id=follower_id)

        follower_name = self.request.query_params.get('follower_name', None)
        if follower_name is not None:
            queryset = queryset.filter(follow_follower__name__contains=follower_name)

        follower_username = self.request.query_params.get('follower_username', None)
        if follower_username is not None:
            queryset = queryset.filter(follow_follower__identity_user__username__contains=follower_username)

        return queryset

    def get_serializer_class(self):
        return FollowSerializer


class AbilityViewset(BaseModelViewSet):
    # queryset = Ability.objects.all()
    owner_field = 'ability_organization'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Ability.objects.filter(delete_flag=False)

        """
            Organizations Filter Options
        """
        organization_id = self.request.query_params.get('organization_id', None)
        if organization_id is not None:
            queryset = queryset.filter(ability_organization_id=organization_id)

        organization_username = self.request.query_params.get('organization_username', None)
        if organization_username is not None:
            queryset = queryset.filter(ability_organization__username__contains=organization_username)

        organization_official_name = self.request.query_params.get('organization_official_name', None)
        if organization_official_name is not None:
            queryset = queryset.filter(ability_organization__official_name__contains=organization_official_name)

        organization_nike_name = self.request.query_params.get('organization_nike_name', None)
        if organization_official_name is not None:
            queryset = queryset.filter(ability_organization__nike_name__contains=organization_nike_name)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        text = self.request.query_params.get('text', None)
        if text is not None:
            queryset = queryset.filter(text__contains=text)

        return queryset

    def get_serializer_class(self):
        return AbilitySerializer


class ConfirmationViewset(BaseModelViewSet):
    # queryset = Confirmation.objects.all()
    permission_classes = [IsAuthenticated, ConfirmationOwner]

    def get_queryset(self):
        queryset = Confirmation.objects.filter(delete_flag=False)

        """
            Corroborant Filter Options
        """
        corroborant_id = self.request.query_params.get('corroborant_id', None)
        if corroborant_id is not None:
            queryset = queryset.filter(confirmation_corroborant_id=corroborant_id)

        corroborant_name = self.request.query_params.get('corroborant_name', None)
        if corroborant_name is not None:
            queryset = queryset.filter(confirmation_corroborant__name__contains=corroborant_name)

        corroborant_username = self.request.query_params.get('corroborant_username', None)
        if corroborant_username is not None:
            queryset = queryset.filter(confirmation_corroborant__identity_user__username__contains=corroborant_username)

        """
            Confirmed Filter Options
        """
        confirmed_id = self.request.query_params.get('confirmed_id', None)
        if confirmed_id is not None:
            queryset = queryset.filter(confirmation_confirmed_id=confirmed_id)

        confirmed_name = self.request.query_params.get('confirmed_name', None)
        if confirmed_name is not None:
            queryset = queryset.filter(confirmation_confirmed__name__contains=confirmed_name)

        confirmed_username = self.request.query_params.get('confirmed_username', None)
        if confirmed_username is not None:
            queryset = queryset.filter(confirmation_confirmed__identity_user__username__contains=confirmed_username)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        link = self.request.query_params.get('link', None)
        if link is not None:
            queryset = queryset.filter(link=link)

        confirm_flag = self.request.query_params.get('confirm_flag', None)
        if confirm_flag is not None:
            queryset = queryset.filter(confirm_flag=confirm_flag)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ConfirmationListViewSerializer
        return ConfirmationSerializer


class CustomerViewset(BaseModelViewSet):
    # queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated, CustomerOrganizationOwner]

    def get_queryset(self):
        queryset = Customer.objects.filter(delete_flag=False)

        """
            Related Customer Filter Options
        """
        related_customer_id = self.request.query_params.get('related_customer_id', None)
        if related_customer_id is not None:
            queryset = queryset.filter(related_customer_id=related_customer_id)

        related_customer_name = self.request.query_params.get('related_customer_name', None)
        if related_customer_name is not None:
            queryset = queryset.filter(related_customer__name__contains=related_customer_name)

        related_customer_user_username = self.request.query_params.get('related_customer_user_username', None)
        if related_customer_user_username is not None:
            queryset = queryset.filter(
                related_customer__identity_user__username__contains=related_customer_user_username)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        return queryset

    def get_serializer_class(self):
        return CustomerSerializer


class MetaDataViewSet(BaseModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = MetaData.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return MetaDataSerializer