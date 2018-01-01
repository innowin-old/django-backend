from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import OrganizationOwner
from .models import (
        Organization,
        StaffCount,
        OrganizationPicture,
        Post,
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
        PostSerializer,
        StaffSerializer,
        FollowSerializer,
        AbilitySerializer,
        ConfirmationSerializer,
        CustomerSerializer
    )


class OrganizationViewset(ModelViewSet):
    queryset = Organization.objects.all()
    permission_classes = [IsAuthenticated, OrganizationOwner]

    def get_queryset(self):
        queryset = Organization.objects.all()

        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner_id=owner)

        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)

        nike_name = self.request.query_params.get('nike_name', None)
        if nike_name is not None:
            queryset = queryset.filter(nike_name=nike_name)

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
            queryset = queryset.filter(registrar_organization=registrar_organization)

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


class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Post.objects.all()

        organization = self.request.query_params.get('organization', None)
        if organization is not None:
            queryset = queryset.filter(organization_id=organization)

        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(user_id=user)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        type = self.request.query_params.get('type', None)
        if type is not None:
            queryset = queryset.filter(type=type)

        return queryset

    def get_serializer_class(self):
        return PostSerializer


class StaffViewset(ModelViewSet):
    queryset = Staff.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Staff.objects.all()

        organization = self.request.query_params.get('organization', None)
        if organization is not None:
            queryset = queryset.filter(organization_id=organization)

        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(user_id=user)

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

        identity = self.request.query_params.get('identity', None)
        if identity is not None:
            queryset = queryset.filter(identity_id=identity)

        follower = self.request.query_params.get('follower', None)
        if follower is not None:
            queryset = queryset.filter(follower_id=follower)

        return queryset

    def get_serializer_class(self):
        return FollowSerializer


class AbilityViewset(ModelViewSet):
    queryset = Ability.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Ability.objects.all()

        organization = self.request.query_params.get('organization', None)
        if organization is not None:
            queryset = queryset.filter(organization_id=organization)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return AbilitySerializer


class ConfirmationViewset(ModelViewSet):
    queryset = Confirmation.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Confirmation.objects.all()

        corroborant = self.request.query_params.get('corroborant', None)
        if corroborant is not None:
            queryset = queryset.filter(corroborant_id=corroborant)

        confirmed = self.request.query_params.get('confirmed', None)
        if confirmed is not None:
            queryset = queryset.filter(confirmed_id=confirmed)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

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

        related_customer = self.request.query_params.get('related_customer', None)
        if related_customer is not None:
            queryset = queryset.filter(related_customer_id=related_customer)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return CustomerSerializer
