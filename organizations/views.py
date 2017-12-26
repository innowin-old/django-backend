from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import (
    Organization,
    StaffCount,
    OrganizationPicture,
    Staff,
    Follow,
    Ability,
    Confirmation,
    Customer
)

from .serializers import (
    OrganizationSerializer,
    StaffCountSerializer,
    OrganizationPictureSerializer,
    StaffSerializer,
    FollowSerializer,
    AbilitySerializer,
    ConfirmationSerializer,
    CustomerSerializer
)


class OrganizationViewset(ModelViewSet):
    queryset = Organization.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Organization.objects.all()

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
        return OrganizationSerializer


class StaffCountViewset(ModelViewSet):
    queryset = StaffCount.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = StaffCount.objects.all()

        organization = self.request.query_params.get('organization', None)
        if organization is not None:
            queryset = queryset.filter(organization_id=organization)

        return queryset

    def get_serializer_class(self):
        return StaffCountSerializer


class OrganizationPictureViewset(ModelViewSet):
    queryset = OrganizationPicture.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = OrganizationPicture.objects.all()

        organization = self.request.query_params.get('organization', None)
        if organization is not None:
            queryset = queryset.filter(organization_id=organization)

        return queryset

    def get_serializer_class(self):
        return OrganizationPictureSerializer


class StaffViewset(ModelViewSet):
    queryset = Staff.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Staff.objects.all()

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
        return StaffSerializer


class FollowViewset(ModelViewSet):
    queryset = Follow.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Follow.objects.all()

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


class AbilityViewset(ModelViewSet):
    queryset = Ability.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Ability.objects.all()

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


class ConfirmationViewset(ModelViewSet):
    queryset = Confirmation.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Confirmation.objects.all()

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
        return ConfirmationSerializer


class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Customer.objects.all()

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
            queryset = queryset.filter(related_customer__identity_user__username__contains=related_customer_user_username)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        return queryset

    def get_serializer_class(self):
        return CustomerSerializer
