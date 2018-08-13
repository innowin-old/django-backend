from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import list_route
from rest_framework.response import Response

import json

from base.permissions import IsOwnerOrReadOnly
from base.views import BaseModelViewSet

from .permissions import (
    IsStaffOrganizationOwnerOrReadOnly,
    IsStaffCountOrganizationOwnerOrReadOnly,
    IsPictureOrganizationOwnerOrReadOnly,
    IsCustomerOrganizationOwner,
    IsConfirmationOwner,
    IsMetaDataOrganizationOwner,
    IsAbilityOrganizationOwnerOrReadOnly,
    IsAdminUserOrCanNotActive,
    IsAdminUserOrCanNotCreateAccepted,
    IsFollowedOrReadOnly,
    IsAdminOrCanNotChangeIdentities,
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
    OrganizationGetObjectSerializer,
    StaffCountSerializer,
    OrganizationPictureSerializer,
    StaffSerializer,
    StaffListViewSerializer,
    FollowSerializer,
    AbilitySerializer,
    ConfirmationSerializer,
    ConfirmationListViewSerializer,
    CustomerSerializer,
    MetaDataSerializer,
    FollowListSerializer)


class OrganizationViewset(BaseModelViewSet):
    owner_field = 'owner'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsAdminUserOrCanNotActive]

    def get_queryset(self):
        queryset = Organization.objects.filter(delete_flag=False)

        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner_id=owner)

        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)

        nike_name = self.request.query_params.get('nike_name', None)
        if nike_name is not None:
            queryset = queryset.filter(nike_name__contains=nike_name)

        official_name = self.request.query_params.get('official_name', None)
        if official_name is not None:
            queryset = queryset.filter(official_name=official_name)

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

        # only admin users can filter active organizations
        if self.request.user.is_superuser:
            active_flag = self.request.query_params.get('active_flag', None)
            if active_flag is not None:
                queryset = queryset.filter(active_flag=active_flag)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return OrganizationListViewSerializer
        elif self.action == 'read':
            return OrganizationGetObjectSerializer
        return OrganizationSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(
        permission_classes=[IsAuthenticated],
        methods=['post']
    )
    def count(self, request):
        organization_id = request.POST.get('organization_id', None)
        if organization_id is not None:
            if organization_id.isdigit():
                try:
                    organization = Organization.objects.get(pk=organization_id)
                except Organization.DoesNotExist:
                    return Response({'detail': "Not found."}, status=status.HTTP_404_NOT_FOUND)
                followers_count = Follow.objects.filter(follow_followed=organization).count()
                return Response({'count': followers_count}, status=status.HTTP_200_OK)
            return Response({'detail': "organization id must be numeric"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"username": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(
        permission_classes=[IsAuthenticated],
        methods=['get']
    )
    def get_meta_data(self, request):
        organization = Organization()
        response = {
            'ownership_types': organization.OWNERSHIP_TYPES,
            'business_types': organization.BUSINESS_TYPES
        }
        return Response(response, status=status.HTTP_200_OK)

    @list_route(
        permission_classes=[IsAdminUser],
        methods=['post'])
    def import_organizations(self, request):
        jsonString = request.data.get('records', None)
        data = json.loads(jsonString)
        errors = []
        for record in data:
            organization = None
            owner = record.get('owner', None)
            if owner is not None:
                try:
                    owner = User.objects.get(username=record.get('owner', None))
                except Exception as e:
                    errors.append({
                        'data': record,
                        'status': str(e)
                    })
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
                    owner=owner
                )
            except Exception as e:
                errors.append({
                    'data': record,
                    'status': str(e)
                })
            if organization is not None:
                phone_data = record.get('phones', None)
                if phone_data is not None:
                    phones = phone_data.split('*')
                    for phone in phones:
                        try:
                            organization_phone = MetaData.objects.create(
                                meta_organization=organization,
                                meta_value=phone,
                                meta_type='phone'
                            )
                        except Exception as e:
                            errors.append({
                                'data': record,
                                'status': str(e)
                            })
                    address_data = record.get('addresses', None)
                if address_data is not None:
                    addresses = address_data.split('*')
                    for address in addresses:
                        try:
                            organization_address = MetaData.objects.create(
                                meta_identity=organization,
                                meta_value=address,
                                meta_type='address'
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
    permission_classes = [IsAuthenticated, IsStaffCountOrganizationOwnerOrReadOnly]

    def get_queryset(self):
        queryset = StaffCount.objects.filter(delete_flag=False)

        organization_id = self.request.query_params.get('organization_id', None)
        if organization_id is not None:
            queryset = queryset.filter(staff_count_organization_id=organization_id)

        organization_nike_name = self.request.query_params.get('organization_nike_name', None)
        if organization_nike_name is not None:
            queryset = queryset.filter(staff_count_organization__nike_name__contains=organization_nike_name)

        organization_username = self.request.query_params.get('organization_username', None)
        if organization_username is not None:
            queryset = queryset.filter(staff_count_organization__username=organization_username)

        return queryset

    def get_serializer_class(self):
        return StaffCountSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizationPictureViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsPictureOrganizationOwnerOrReadOnly]

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
            queryset = queryset.filter(staff_count_organization__username=organization_username)

        return queryset

    def get_serializer_class(self):
        return OrganizationPictureSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsStaffOrganizationOwnerOrReadOnly]

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
            queryset = queryset.filter(staff_organization__username=organization_username)

        organization_official_name = self.request.query_params.get('organization_official_name', None)
        if organization_official_name is not None:
            queryset = queryset.filter(staff_organization__official_name=organization_official_name)

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
            queryset = queryset.filter(staff_user__username=user_username)

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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUserOrCanNotCreateAccepted, IsFollowedOrReadOnly,
                          IsAdminOrCanNotChangeIdentities]

    def get_queryset(self):
        queryset = Follow.objects.filter(delete_flag=False)

        """
            Followed Filter Options
        """
        follow_followed_id = self.request.query_params.get('follow_followed', None)
        if follow_followed_id is not None:
            queryset = queryset.filter(follow_followed_id=follow_followed_id)

        follow_followed_name = self.request.query_params.get('follow_followed_name', None)
        if follow_followed_name is not None:
            queryset = queryset.filter(follow_followed__name=follow_followed_name)

        follow_followed_user_username = self.request.query_params.get('follow_followed_user_username', None)
        if follow_followed_user_username is not None:
            queryset = queryset.filter(follow_identity__identity_user__username=follow_followed_user_username)

        """
            Follower Filter Options
        """
        follower_id = self.request.query_params.get('follow_follower', None)
        if follower_id is not None:
            queryset = queryset.filter(follow_follower_id=follower_id)

        follower_name = self.request.query_params.get('follow_follower_name', None)
        if follower_name is not None:
            queryset = queryset.filter(follow_follower__name__contains=follower_name)

        follower_username = self.request.query_params.get('follow_follower_username', None)
        if follower_username is not None:
            queryset = queryset.filter(follow_follower__identity_user__username=follower_username)

        """
            Accept Filter
        """
        follow_accepted = self.request.query_params.get('follow_accepted', None)
        if follow_accepted is not None:
            queryset = queryset.filter(follow_accepted=follow_accepted)

        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return FollowListSerializer
        return FollowSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class AbilityViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsAbilityOrganizationOwnerOrReadOnly]

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
            queryset = queryset.filter(ability_organization__username=organization_username)

        organization_official_name = self.request.query_params.get('organization_official_name', None)
        if organization_official_name is not None:
            queryset = queryset.filter(ability_organization__official_name=organization_official_name)

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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConfirmationViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsConfirmationOwner]

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
            queryset = queryset.filter(confirmation_corroborant__identity_user__username=corroborant_username)

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
            queryset = queryset.filter(confirmation_confirmed__identity_user__username=confirmed_username)

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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsCustomerOrganizationOwner]

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
                related_customer__identity_user__username=related_customer_user_username)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        return queryset

    def get_serializer_class(self):
        return CustomerSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class MetaDataViewSet(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsMetaDataOrganizationOwner]

    def get_queryset(self):
        queryset = MetaData.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return MetaDataSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
